# v0.8 no-auth sources

No procurement connector credentials are required. Only application login variables are used.

- TED: anonymous access to published-notice search.
- Prozorro: public API feed plus tender detail endpoint. `tenderID` is the displayed unique number.
- Germany: anonymous daily OCDS ZIP export.
- Poland: anonymous BZP notice reading endpoint.

France BOAMP and Italy ANAC are not enabled in this build because the exact production query/base URL and tested response mapping were not fully verified in the gathered official documentation. Spain, Baltics and Slovenia are also excluded rather than represented by fragile HTML scrapers.
