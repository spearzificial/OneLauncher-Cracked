use oneclient_app::updater::CrackedVersion;

#[test]
fn test_version_2_9_0_c1_upgrade_progression() {
    let v280 = CrackedVersion::parse("2.8.0-c1").expect("parse 2.8.0-c1");
    let v290 = CrackedVersion::parse("2.9.0-c1").expect("parse 2.9.0-c1");

    assert!(v290 > v280, "2.9.0-c1 must be greater than 2.8.0-c1");
    assert_eq!(
        v290,
        CrackedVersion {
            major: 2,
            minor: 9,
            patch: 0,
            rev: 1,
        }
    );

    // Assert that the workspace cargo package version is updated to 2.9.0-c1
    assert_eq!(
        env!("CARGO_PKG_VERSION"),
        "2.9.0-c1",
        "Cargo.toml must be 2.9.0-c1"
    );
}
