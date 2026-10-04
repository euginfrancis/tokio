#![warn(rust_2018_idioms)]
#![cfg(feature = "full")]
#![cfg(unix)]

// Repro for tokio-rs/tokio#8516. `UnixStream::pair()` has no peer credentials on
// NetBSD, so the existing test in `uds_cred.rs` never reaches the kernel path.
// Sockets that go through bind/listen/accept/connect do carry credentials, and
// on NetBSD `peer_cred()` fails with ENOPROTOOPT because `LOCAL_PEEREID` is
// queried at `SOL_SOCKET` instead of `SOL_LOCAL`.

use tokio::net::{UnixListener, UnixStream};

#[tokio::test]
async fn peer_cred_on_connected_sockets() {
    let dir = tempfile::tempdir().unwrap();
    let path = dir.path().join("sock");

    let listener = UnixListener::bind(&path).unwrap();
    let (client, accepted) = tokio::join!(UnixStream::connect(&path), listener.accept());
    let client = client.unwrap();
    let (server, _) = accepted.unwrap();

    let uid = unsafe { libc::getuid() };
    let gid = unsafe { libc::getgid() };

    for (name, sock) in [("client", &client), ("accepted", &server)] {
        let cred = sock
            .peer_cred()
            .unwrap_or_else(|e| panic!("{name}: peer_cred() failed: {e}"));
        assert_eq!(cred.uid(), uid, "{name}");
        assert_eq!(cred.gid(), gid, "{name}");
        assert_eq!(cred.pid(), Some(std::process::id() as _), "{name}");
    }
}
