from app.sources import sources_for
def test_source_routing():
 assert sources_for(['UKR'])==[('prozorro',['UKR'])]
 assert sources_for(['POL'])[0][0]=='ted'
 assert len(sources_for(['POL','UKR']))==3
