use oneclient_app::updater::CrackedVersion;

#[test]
fn test_version_2_10_1_c1_upgrade_progression() {
    let v290 = CrackedVersion::parse("2.9.0-c1").expect("parse 2.9.0-c1");
    let v2101 = CrackedVersion::parse("2.10.1-c1").expect("parse 2.10.1-c1");

    assert!(v2101 > v290, "2.10.1-c1 must be greater than 2.9.0-c1");
    assert_eq!(
        v2101,
        CrackedVersion {
            major: 2,
            minor: 10,
            patch: 1,
            rev: 1,
        }
    );

    // Assert that the workspace cargo package version is updated to 2.10.1-c1
    assert_eq!(
        env!("CARGO_PKG_VERSION"),
        "2.10.1-c1",
        "Cargo.toml must be 2.10.1-c1"
    );
}
