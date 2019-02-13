from robotoff.insights.annotate import InsightAnnotatorFactory
from robotoff.models import ProductInsight


insight_type = 'label'
annotator = InsightAnnotatorFactory.create(insight_type)


AUTHORIZED_LABELS = {
    "AT-BIO-301",
    "AT-BIO-402",
    "AT-BIO-901",
    "AT-BIO-902",
    "BE-BIO-01",
    "BE-BIO-02",
    "BG-BIO-15",
    "BG-BIO-16",
    "CH-BIO-004",
    "CH-BIO-006",
    "CH-BIO-086",
    "CZ-BIO-001",
    "CZ-BIO-002",
    "DE-ÖKO-001",
    "DE-ÖKO-003",
    "DE-ÖKO-005",
    "DE-ÖKO-006",
    "DE-ÖKO-007",
    "DE-ÖKO-009",
    "DE-ÖKO-012",
    "DE-ÖKO-013",
    "DE-ÖKO-021",
    "DE-ÖKO-024",
    "DE-ÖKO-034",
    "DE-ÖKO-037",
    "DE-ÖKO-039",
    "DE-ÖKO-060",
    "DE-ÖKO-064",
    "DE-ÖKO-070",
    "FR-BIO-01",
    "FR-BIO-07",
    "FR-BIO-09",
    "FR-BIO-10",
    "FR-BIO-11",
    "FR-BIO-12",
    "FR-BIO-13",
    "FR-BIO-15",
    "FR-BIO-16",
    "GR-BIO-01",
    "GR-BIO-02",
    "GR-BIO-03",
    "IT-BIO-003",
    "IT-BIO-004",
    "IT-BIO-005",
    "IT-BIO-006",
    "IT-BIO-007",
    "IT-BIO-008",
    "IT-BIO-009",
    "IT-BIO-013",
    "IT-BIO-014",
    "LU-BIO-04",
    "NL-BIO-01",
    "PT-BIO-02",
    "PT-BIO-04",
    "VN-BIO-154",
}

i = 0
for insight in ProductInsight.select().where(ProductInsight.type == insight_type,
                                             ProductInsight.annotation.is_null()):
    i += 1
    print("Insight %d" % i)

    if insight.data['label_tag'] not in AUTHORIZED_LABELS:
        continue

    print("Add label {} to https://fr.openfoodfacts.org/produit/{}".format(insight.data['label_tag'],
                                                                           insight.barcode))
    print(insight.data)
    annotator.save_annotation(insight)
    insight.annotation = 1
    insight.save()