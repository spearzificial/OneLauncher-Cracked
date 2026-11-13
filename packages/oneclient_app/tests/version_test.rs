use oneclient_app::updater::CrackedVersion;

#[test]
fn test_version_2_10_1_c2_upgrade_progression() {
    let v2101_c1 = CrackedVersion::parse("2.10.1-c1").expect("parse 2.10.1-c1");
    let v2101_c2 = CrackedVersion::parse("2.10.1-c2").expect("parse 2.10.1-c2");

    assert!(v2101_c2 > v2101_c1, "2.10.1-c2 must be greater than 2.10.1-c1");
    assert_eq!(
        v2101_c2,
        CrackedVersion {
            major: 2,
            minor: 10,
            patch: 1,
            rev: 2,
        }
    );

    // Assert that the workspace cargo package version is updated to 2.10.1-c2
    assert_eq!(
        env!("CARGO_PKG_VERSION"),
        "2.10.1-c2",
        "Cargo.toml must be 2.10.1-c2"
    );
}
