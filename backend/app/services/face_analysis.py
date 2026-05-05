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

            # Use landmarks if available, otherwise fall back to percentages
            if landmarks:
                # Get exact eye coordinates from Mediapipe
                lm = landmarks.landmark

                # Left eye corners
                l_left  = (int(lm[33].x * w),  int(lm[33].y * h))
                l_right = (int(lm[133].x * w), int(lm[133].y * h))
                l_top   = (int(lm[159].x * w), int(lm[159].y * h))
                l_bot   = (int(lm[145].x * w), int(lm[145].y * h))

                # Right eye corners
                r_left  = (int(lm[362].x * w), int(lm[362].y * h))
                r_right = (int(lm[263].x * w), int(lm[263].y * h))
                r_top   = (int(lm[386].x * w), int(lm[386].y * h))
                r_bot   = (int(lm[374].x * w), int(lm[374].y * h))

                # Add padding around eye region
                pad = 10

                # Crop left eye region
                left_eye = image_bgr[
                    max(0, l_top[1] - pad) : min(h, l_bot[1] + pad),
                    max(0, l_left[0] - pad) : min(w, l_right[0] + pad)
                ]

                # Crop right eye region
                right_eye = image_bgr[
                    max(0, r_top[1] - pad) : min(h, r_bot[1] + pad),
                    max(0, r_left[0] - pad) : min(w, r_right[0] + pad)
                ]

                # Combine both eyes
                eye_regions = [r for r in [left_eye, right_eye] if r.size > 0]

                if not eye_regions:
                    return {"detected": False, "confidence": 0.0, "note": "Could not extract eye region"}

                # Analyze redness in both eyes
                redness_scores = []
                for eye in eye_regions:
                    b, g, r = cv2.split(eye)
                    avg_r = float(np.mean(r))
                    avg_g = float(np.mean(g))
                    avg_b = float(np.mean(b))
                    redness_scores.append(avg_r / (avg_g + avg_b + 1e-5))

                redness_score = float(np.mean(redness_scores))

            else:
                # Fallback to percentage if no landmarks
                eye_region = image_bgr[
                    int(0.25 * h): int(0.45 * h),
                    int(0.20 * w): int(0.80 * w)
                ]
                b, g, r = cv2.split(eye_region)
                redness_score = float(np.mean(r)) / (float(np.mean(g)) + float(np.mean(b)) + 1e-5)

            detected = redness_score > 0.38

            return {
                "detected": detected,
                "confidence": round(min(redness_score, 1.0), 2),
                "note": "Possible eye redness detected" if detected else "No significant eye redness"
            }
        except Exception as e:
            logger.error(f"Eye redness analysis error: {e}")
            return {"detected": False, "confidence": 0.0, "note": "Analysis failed"}
        
    def _analyze_pale_skin(self, image_bgr, landmarks) -> Dict:
        try:
            h, w = image_bgr.shape[:2]

            if landmarks:
                lm = landmarks.landmark

                # Use exact cheek landmarks
                left_cheek  = (int(lm[187].x * w), int(lm[187].y * h))
                right_cheek = (int(lm[411].x * w), int(lm[411].y * h))

                pad = 20

                # Crop left cheek region
                left_region = image_bgr[
                    max(0, left_cheek[1] - pad) : min(h, left_cheek[1] + pad),
                    max(0, left_cheek[0] - pad) : min(w, left_cheek[0] + pad)
                ]

                # Crop right cheek region
                right_region = image_bgr[
                    max(0, right_cheek[1] - pad) : min(h, right_cheek[1] + pad),
                    max(0, right_cheek[0] - pad) : min(w, right_cheek[0] + pad)
                ]

                # Combine both cheeks
                regions = [r for r in [left_region, right_region] if r.size > 0]

                if not regions:
                    return {"detected": False, "confidence": 0.0, "note": "Could not extract skin region"}

                # Measure saturation of both cheeks
                saturations = []
                for region in regions:
                    hsv = cv2.cvtColor(region, cv2.COLOR_BGR2HSV)
                    saturations.append(float(np.mean(hsv[:, :, 1])))

                avg_saturation = float(np.mean(saturations))

            else:
                # Fallback
                cheek_region = image_bgr[
                    int(0.40 * h): int(0.65 * h),
                    int(0.25 * w): int(0.75 * w)
                ]
                hsv = cv2.cvtColor(cheek_region, cv2.COLOR_BGR2HSV)
                avg_saturation = float(np.mean(hsv[:, :, 1]))

            # print(f"DEBUG pale skin avg_saturation: {avg_saturation}")

            detected = avg_saturation < 80

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

            if landmarks:
                lm = landmarks.landmark

                # Exact under-eye landmarks
                left_under  = (int(lm[253].x * w), int(lm[253].y * h))
                right_under = (int(lm[380].x * w), int(lm[380].y * h))

                # Exact cheek landmarks for reference brightness
                left_cheek  = (int(lm[187].x * w), int(lm[187].y * h))
                right_cheek = (int(lm[411].x * w), int(lm[411].y * h))

                pad = 15

                # Crop under eye regions
                left_under_region = image_bgr[
                    max(0, left_under[1] - pad) : min(h, left_under[1] + pad),
                    max(0, left_under[0] - pad) : min(w, left_under[0] + pad)
                ]
                right_under_region = image_bgr[
                    max(0, right_under[1] - pad) : min(h, right_under[1] + pad),
                    max(0, right_under[0] - pad) : min(w, right_under[0] + pad)
                ]

                # Crop cheek regions
                left_cheek_region = image_bgr[
                    max(0, left_cheek[1] - pad) : min(h, left_cheek[1] + pad),
                    max(0, left_cheek[0] - pad) : min(w, left_cheek[0] + pad)
                ]
                right_cheek_region = image_bgr[
                    max(0, right_cheek[1] - pad) : min(h, right_cheek[1] + pad),
                    max(0, right_cheek[0] - pad) : min(w, right_cheek[0] + pad)
                ]

                # Measure brightness of under-eye vs cheeks
                under_regions = [r for r in [left_under_region, right_under_region] if r.size > 0]
                cheek_regions = [r for r in [left_cheek_region, right_cheek_region] if r.size > 0]

                if not under_regions or not cheek_regions:
                    return {"detected": False, "confidence": 0.0, "note": "Could not extract regions"}

                under_brightness = float(np.mean([
                    np.mean(cv2.cvtColor(r, cv2.COLOR_BGR2GRAY)) 
                    for r in under_regions
                ]))
                cheek_brightness = float(np.mean([
                    np.mean(cv2.cvtColor(r, cv2.COLOR_BGR2GRAY)) 
                    for r in cheek_regions
                ]))

            else:
                # Fallback
                under_eye = image_bgr[int(0.42*h):int(0.52*h), int(0.25*w):int(0.75*w)]
                cheek     = image_bgr[int(0.55*h):int(0.70*h), int(0.25*w):int(0.75*w)]
                under_brightness = float(np.mean(cv2.cvtColor(under_eye, cv2.COLOR_BGR2GRAY)))
                cheek_brightness = float(np.mean(cv2.cvtColor(cheek, cv2.COLOR_BGR2GRAY)))

            brightness_diff = cheek_brightness - under_brightness
            # print(f"DEBUG dark circles brightness_diff: {brightness_diff}")

            detected = brightness_diff > 10
            confidence = round(max(0.0, min(brightness_diff / 80, 1.0)), 2)

            return {
                "detected": detected,
                "confidence": confidence,
                "note": "Possible dark circles detected" if detected else "No significant dark circles"
            }
        except Exception as e:
            logger.error(f"Dark circles analysis error: {e}")
            return {"detected": False, "confidence": 0.0, "note": "Analysis failed"}

    def _analyze_fatigue(self, indicators: Dict) -> Dict:
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
        return {
            "face_detected": False,
            "indicators": {},
            "overall_summary": [f"Face analysis unavailable: {reason}"],
            "disclaimer": "These results are informational only and not a medical diagnosis."
        }