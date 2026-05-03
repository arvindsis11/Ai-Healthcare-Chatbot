import base64
import logging
from dataclasses import dataclass
from typing import List, Dict
import numpy as np

try:
    import cv2
except ImportError:
    cv2 = None

try:
    import mediapipe as mp
except ImportError:
    mp = None

logger = logging.getLogger(__name__)


@dataclass
class FaceAnalysisService:
    """
    Analyzes facial indicators to detect potential health issues.
    NOTE: Results are informational only, not medical diagnosis.
    """
    def analyze(self, image_base64: str) -> Dict:
        """
        Main function — takes a base64 image string, returns health indicators.
        """
        # Step 1 — Check if OpenCV is available
        if cv2 is None:
            return self._unavailable_response("opencv-python not installed")

        # Step 2 — Decode base64 string → bytes → numpy array → OpenCV image
        try:
            image_data = base64.b64decode(image_base64)
            np_array = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

            if image is None:
                return self._error_response("Could not decode image.")
        except Exception as e:
            logger.error(f"Image decode error: {e}")
            return self._error_response("Invalid image format.")
        
        # Step 3 — Convert BGR to RGB for Mediapipe
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Step 4 — Detect face
        face_detected, landmarks = self._detect_face(image_rgb)

        if not face_detected:
            return self._error_response("No face detected. Please upload a clear front-facing photo.")
        
    # Step 5 — Run each health indicator analysis
        indicators = {}
        indicators["eye_redness"]    = self._analyze_eye_redness(image, landmarks)
        indicators["pale_skin"]      = self._analyze_pale_skin(image, landmarks)
        indicators["dark_circles"]   = self._analyze_dark_circles(image, landmarks)
        indicators["fatigue"]        = self._analyze_fatigue(indicators)

        # Step 6 — Return final result
        return {
            "face_detected": True,
            "indicators": indicators,
            "overall_summary": self._build_summary(indicators),
            "disclaimer": "These results are informational only and not a medical diagnosis."
        }
    
    def _detect_face(self, image_rgb):
        """Returns (face_detected: bool, landmarks or None)"""
        if mp is None:
            return self._detect_face_opencv(image_rgb), None

        mp_face_mesh = mp.solutions.face_mesh
        with mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5
        ) as face_mesh:
            results = face_mesh.process(image_rgb)
            if results.multi_face_landmarks:
                return True, results.multi_face_landmarks[0]
            return False, None

    def _detect_face_opencv(self, image_rgb):
        """Fallback face detection using OpenCV Haar Cascade"""
        image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        return len(faces) > 0
    
    def _analyze_eye_redness(self, image_bgr, landmarks) -> Dict:
        try:
            h, w = image_bgr.shape[:2]
            
            eye_region = image_bgr[
                int(0.25 * h) : int(0.45 * h),
                int(0.20 * w) : int(0.80 * w)
            ]
            
            if eye_region.size == 0:
                return {"detected": False, "confidence": 0.0, "note": "Could not extract eye region"}
            
            b, g, r = cv2.split(eye_region)
            
            avg_r = float(np.mean(r))
            avg_g = float(np.mean(g))
            avg_b = float(np.mean(b))
            
            redness_score = avg_r / (avg_g + avg_b + 1e-5)
            
            detected = redness_score > 0.38
            
            return {
                "detected": detected,
                "confidence": round(redness_score, 2),
                "note": "Possible eye redness detected" if detected else "No significant eye redness"
            }
        except Exception as e:
            logger.error(f"Eye redness analysis error: {e}")
            return {"detected": False, "confidence": 0.0, "note": "Analysis failed"}
        
        
    def _analyze_pale_skin(self, image_bgr, landmarks) -> Dict:
        try:
            h, w = image_bgr.shape[:2]

            cheek_region = image_bgr[
                int(0.40 * h): int(0.65 * h),
                int(0.25 * w): int(0.75 * w)
            ]

            if cheek_region.size == 0:
                return {"detected": False, "confidence": 0.0, "note": "Could not extract skin region"}

            # Convert to HSV — S channel tells us color vividness
            hsv = cv2.cvtColor(cheek_region, cv2.COLOR_BGR2HSV)
            saturation = hsv[:, :, 1]   # index 1 = S channel

            avg_saturation = float(np.mean(saturation))

            # Low saturation = pale skin
            detected = avg_saturation < 40

            return {
                "detected": detected,
                "confidence": round(1 - (avg_saturation / 255), 2),
                "note": "Possible pale skin detected" if detected else "Skin tone appears normal"
            }
        except Exception as e:
            logger.error(f"Pale skin analysis error: {e}")
            return {"detected": False, "confidence": 0.0, "note": "Analysis failed"}


    def _analyze_dark_circles(self, image_bgr, landmarks) -> Dict:
        try:
            h, w = image_bgr.shape[:2]

            # Under eye region
            under_eye = image_bgr[
                int(0.42 * h): int(0.52 * h),
                int(0.25 * w): int(0.75 * w)
            ]

            # Cheek region — reference brightness
            cheek = image_bgr[
                int(0.55 * h): int(0.70 * h),
                int(0.25 * w): int(0.75 * w)
            ]

            if under_eye.size == 0 or cheek.size == 0:
                return {"detected": False, "confidence": 0.0, "note": "Could not extract regions"}

            # Convert to grayscale — measure brightness only
            under_eye_gray = cv2.cvtColor(under_eye, cv2.COLOR_BGR2GRAY)
            cheek_gray     = cv2.cvtColor(cheek, cv2.COLOR_BGR2GRAY)

            under_eye_brightness = float(np.mean(under_eye_gray))
            cheek_brightness     = float(np.mean(cheek_gray))

            # YOUR idea — compare brightness difference
            brightness_diff = cheek_brightness - under_eye_brightness
            detected = brightness_diff > 20

            confidence = round(min(brightness_diff / 80, 1.0), 2)

            return {
                "detected": detected,
                "confidence": confidence,
                "note": "Possible dark circles detected" if detected else "No significant dark circles"
            }
        except Exception as e:
            logger.error(f"Dark circles analysis error: {e}")
            return {"detected": False, "confidence": 0.0, "note": "Analysis failed"}


    def _analyze_fatigue(self, indicators: Dict) -> Dict:
        # YOUR idea — combine all 3 indicators
        detected_count = sum(
            1 for key in ["eye_redness", "pale_skin", "dark_circles"]
            if indicators.get(key, {}).get("detected", False)
        )

        detected = detected_count >= 2
        confidence = round(detected_count / 3, 2)

        return {
            "detected": detected,
            "confidence": confidence,
            "note": f"{detected_count}/3 fatigue indicators present. {'Possible fatigue detected.' if detected else 'No significant fatigue signs.'}"
        }


    def _build_summary(self, indicators: Dict) -> List[str]:
        summary = []
        for key, data in indicators.items():
            if data.get("detected"):
                summary.append(data.get("note", key))
        if not summary:
            summary.append("No significant health indicators detected.")
        return summary


    def _error_response(self, message: str) -> Dict:
        return {
            "face_detected": False,
            "indicators": {},
            "overall_summary": [message],
            "disclaimer": "These results are informational only and not a medical diagnosis."
        }

    def _unavailable_response(self, reason: str) -> Dict:
        return {
            "face_detected": False,
            "indicators": {},
            "overall_summary": [f"Face analysis unavailable: {reason}"],
            "disclaimer": "These results are informational only and not a medical diagnosis."
        }