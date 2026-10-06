from app.sources import sources_for
def test_all_noauth_routes():
 r=sources_for(['DEU','POL','UKR','FRA']);names=[x[0] for x in r]
 assert names==['ted','prozorro','germany','poland']
