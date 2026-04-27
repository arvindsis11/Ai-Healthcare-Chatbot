import pytest
from scripts.fetch_pubmed_data import parse_pubmed_xml

SAMPLE_XML = """
<PubmedArticleSet>
  <PubmedArticle>
    <MedlineCitation>
      <PMID>12345678</PMID>
      <Article>
        <ArticleTitle>Efficacy of Paracetamol in Children with Fever</ArticleTitle>
        <Abstract>
          <AbstractText>This study demonstrates that paracetamol is effective for reducing fever in children.</AbstractText>
        </Abstract>
        <AuthorList>
          <Author>
            <LastName>Smith</LastName>
            <ForeName>John</ForeName>
          </Author>
        </AuthorList>
        <Journal>
          <JournalIssue>
            <PubDate>
              <Year>2023</Year>
            </PubDate>
          </JournalIssue>
        </Journal>
      </Article>
    </MedlineCitation>
  </PubmedArticle>
</PubmedArticleSet>
"""

def test_parse_pubmed_xml():
    articles = parse_pubmed_xml(SAMPLE_XML)
    assert len(articles) == 1
    article = articles[0]
    
    assert article["title"] == "Efficacy of Paracetamol in Children with Fever"
    assert "paracetamol is effective" in article["content"]
    assert article["metadata"]["pmid"] == "12345678"
    assert article["metadata"]["authors"] == ["John Smith"]
    assert article["metadata"]["year"] == "2023"
    assert article["metadata"]["source"] == "pubmed"

def test_parse_empty_xml():
    articles = parse_pubmed_xml("")
    assert articles == []

def test_parse_malformed_xml():
    # Should handle or log error gracefully
    with pytest.raises(Exception):
        parse_pubmed_xml("<invalid>")
