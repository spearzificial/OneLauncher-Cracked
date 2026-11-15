use oneclient_app::updater::CrackedVersion;

#[test]
fn test_version_2_10_2_c1_upgrade_progression() {
    let previous = CrackedVersion::parse("2.10.1-c2").expect("parse 2.10.1-c2");
    let current = CrackedVersion::parse("2.10.2-c1").expect("parse 2.10.2-c1");

    assert!(current > previous, "2.10.2-c1 must be greater than 2.10.1-c2");
    assert_eq!(
        current,
        CrackedVersion {
            major: 2,
            minor: 10,
            patch: 2,
            rev: 1,
        }
    );

    // Assert that the workspace cargo package version is updated to 2.10.2-c1
    assert_eq!(
        env!("CARGO_PKG_VERSION"),
        "2.10.2-c1",
        "Cargo.toml must be 2.10.2-c1"
    );
}
