from app.core import Tender,Store
from datetime import datetime
def test_ted_national_duplicate_merges():
 s=Store();a=Tender('ted:1','ted','DEU','Supply of SSD drives','City IT',1000,'EUR',datetime(2026,12,1),url='https://ted.europa.eu/notice/123456-2026');b=Tender('de:2','germany','DEU','Supply of SSD drives','City IT',1000,'EUR',datetime(2026,12,1),url='https://local/123456-2026')
 s.add('ted',[a]);s.add('germany',[b]);assert len(s.data)==1;assert set(next(iter(s.data.values())).sources)=={'ted','germany'}
