from app.core import Tender
def test_public_procurement_id_field():
 t=Tender('prozorro:internal','prozorro','UKR','x',procurement_id='UA-2026-01-01-000001-a')
 assert t.procurement_id.startswith('UA-')
