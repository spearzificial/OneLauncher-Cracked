use oneclient_app::updater::CrackedVersion;

#[test]
fn test_version_2_11_0_c2_upgrade_progression() {
    let previous = CrackedVersion::parse("2.11.0-c1").expect("parse 2.11.0-c1");
    let current = CrackedVersion::parse("2.11.0-c2").expect("parse 2.11.0-c2");

    assert!(current > previous, "2.11.0-c2 must be greater than 2.11.0-c1");
    assert_eq!(
        current,
        CrackedVersion {
            major: 2,
            minor: 11,
            patch: 0,
            rev: 2,
        }
    );

    // Assert that the workspace cargo package version is updated to 2.11.0-c2
    assert_eq!(
        env!("CARGO_PKG_VERSION"),
        "2.11.0-c2",
        "Cargo.toml must be 2.11.0-c2"
    );
}
