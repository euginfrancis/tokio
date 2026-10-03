# `tokio::net` — 91 functions

[← index](./README.md)

Flags: 🅰 async · ⚠ unsafe · 🅲 const

| Kind | Count |
|---|---:|
| Public API | 62 |
| Trait impl | 21 |
| Private helper | 6 |
| Crate-internal | 1 |
| Trait method (declaration/default) | 1 |

## `tokio/src/net/addr.rs` (18)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 24 | `to_socket_addrs`  |  | Crate-internal | Conversion |  |
| 43 | `to_socket_addrs`  | `sealed::ToSocketAddrsPriv for &T` | Trait impl | Conversion |  |
| 56 | `to_socket_addrs`  | `sealed::ToSocketAddrsPriv for SocketAddr` | Trait impl | Conversion |  |
| 70 | `to_socket_addrs`  | `sealed::ToSocketAddrsPriv for SocketAddrV4` | Trait impl | Conversion |  |
| 83 | `to_socket_addrs`  | `sealed::ToSocketAddrsPriv for SocketAddrV6` | Trait impl | Conversion |  |
| 96 | `to_socket_addrs`  | `sealed::ToSocketAddrsPriv for (IpAddr, u16)` | Trait impl | Conversion |  |
| 110 | `to_socket_addrs`  | `sealed::ToSocketAddrsPriv for (Ipv4Addr, u16)` | Trait impl | Conversion |  |
| 124 | `to_socket_addrs`  | `sealed::ToSocketAddrsPriv for (Ipv6Addr, u16)` | Trait impl | Conversion |  |
| 138 | `to_socket_addrs`  | `sealed::ToSocketAddrsPriv for &[SocketAddr]` | Trait impl | Conversion |  |
| 140 | `slice_to_vec`  |  | Private helper | Other / internal logic |  |
| 168 | `to_socket_addrs`  | `sealed::ToSocketAddrsPriv for str` | Trait impl | Conversion |  |
| 196 | `to_socket_addrs`  | `sealed::ToSocketAddrsPriv for (&str, u16)` | Trait impl | Conversion |  |
| 233 | `to_socket_addrs`  | `sealed::ToSocketAddrsPriv for (String, u16)` | Trait impl | Conversion |  |
| 246 | `to_socket_addrs`  | `sealed::ToSocketAddrsPriv for String` | Trait impl | Conversion |  |
| 266 | `to_socket_addrs`  | `trait ToSocketAddrsPriv` | Trait method (declaration/default) | Conversion |  |
| 300 | `poll`  | `Future for MaybeReady` | Trait impl | Future impl (poll) |  |
| 318 | `next`  | `Iterator for OneOrMore` | Trait impl | Iterator |  |
| 325 | `size_hint`  | `Iterator for OneOrMore` | Trait impl | Iterator |  |

## `tokio/src/net/lookup_host.rs` (1)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 32 | `lookup_host` 🅰 |  | Public API | Async operation | Performs a DNS resolution. |

## `tokio/src/net/udp.rs` (72)

| Line | Function | On type / trait | Kind | Role | Summary (from its docs) |
|---:|---|---|---|---|---|
| 150 | `bind` 🅰 | `UdpSocket` | Public API | Networking | This function will create a new UDP socket and attempt to bind it to the `addr` provided. |
| 169 | `bind_addr`  | `UdpSocket` | Private helper | Networking |  |
| 175 | `new`  | `UdpSocket` | Private helper | Constructor |  |
| 227 | `from_std`  | `UdpSocket` | Public API | Conversion | Creates new `UdpSocket` from a previously bound `std::net::UdpSocket`. |
| 256 | `into_std`  | `UdpSocket` | Public API | Conversion | Turns a [`tokio::net::UdpSocket`] into a [`std::net::UdpSocket`]. |
| 276 | `as_socket`  | `UdpSocket` | Private helper | Conversion |  |
| 297 | `local_addr`  | `UdpSocket` | Public API | Networking | Returns the local address that this socket is bound to. |
| 320 | `peer_addr`  | `UdpSocket` | Public API | Networking | Returns the socket address of the remote peer this socket was connected to. |
| 348 | `connect` 🅰 | `UdpSocket` | Public API | Networking | Connects the UDP socket setting the default destination for send() and limiting packets that are read via `recv` from the address specified in `addr`. |
| 435 | `ready` 🅰 | `UdpSocket` | Public API | I/O operation | Waits for any of the requested ready states. |
| 490 | `writable` 🅰 | `UdpSocket` | Public API | Async operation | Waits for the socket to become writable. |
| 524 | `poll_send_ready`  | `UdpSocket` | Public API | Poll function | Polls for write/send readiness. |
| 570 | `send` 🅰 | `UdpSocket` | Public API | Data movement | Sends data on the socket to the remote address that the socket is connected to. |
| 600 | `poll_send`  | `UdpSocket` | Public API | Poll function | Attempts to send data on the socket to the remote address to which it was previously `connect`ed. |
| 654 | `try_send`  | `UdpSocket` | Public API | Non-blocking attempt | Tries to send data on the socket to the remote address to which it is connected. |
| 715 | `readable` 🅰 | `UdpSocket` | Public API | I/O operation | Waits for the socket to become readable. |
| 749 | `poll_recv_ready`  | `UdpSocket` | Public API | Poll function | Polls for read/receive readiness. |
| 790 | `recv` 🅰 | `UdpSocket` | Public API | Data movement | Receives a single datagram message on the socket from the remote address to which it is connected. |
| 820 | `poll_recv`  | `UdpSocket` | Public API | Poll function | Attempts to receive a single datagram message on the socket from the remote address to which it is `connect`ed. |
| 889 | `try_recv`  | `UdpSocket` | Public API | Non-blocking attempt | Tries to receive a single datagram message on the socket from the remote address to which it is connected. |
| 945 | `try_recv_buf`  | `UdpSocket` | Public API | Non-blocking attempt | Tries to receive data from the stream into the provided buffer, advancing the buffer's internal cursor, returning how many bytes were read. |
| 993 | `recv_buf` 🅰 | `UdpSocket` | Public API | Data movement | Receives a single datagram message on the socket from the remote address to which it is connected, advancing the buffer's internal cursor, returning how many bytes were read. |
| 1071 | `try_recv_buf_from`  | `UdpSocket` | Public API | Non-blocking attempt | Tries to receive a single datagram message on the socket. |
| 1127 | `recv_buf_from` 🅰 | `UdpSocket` | Public API | Data movement | Receives a single datagram message on the socket, advancing the buffer's internal cursor, returning how many bytes were read and the origin. |
| 1185 | `send_to` 🅰 | `UdpSocket` | Public API | Data movement | Sends data on the socket to the given address. |
| 1214 | `poll_send_to`  | `UdpSocket` | Public API | Poll function | Attempts to send data on the socket to a given address. |
| 1272 | `try_send_to`  | `UdpSocket` | Public API | Non-blocking attempt | Tries to send data on the socket to the given address, but if the send is blocked this will return right away. |
| 1278 | `send_to_addr` 🅰 | `UdpSocket` | Private helper | Data movement |  |
| 1326 | `recv_from` 🅰 | `UdpSocket` | Public API | Data movement | Receives a single datagram message on the socket. |
| 1361 | `poll_recv_from`  | `UdpSocket` | Public API | Poll function | Attempts to receive a single datagram on the socket. |
| 1442 | `try_recv_from`  | `UdpSocket` | Public API | Non-blocking attempt | Tries to receive a single datagram message on the socket. |
| 1480 | `try_io`  | `UdpSocket` | Public API | Non-blocking attempt | Tries to read or write from the socket using a user-provided IO operation. |
| 1515 | `async_io` 🅰 | `UdpSocket` | Public API | Async operation | Reads or writes from the socket using a user-provided IO operation. |
| 1569 | `peek` 🅰 | `UdpSocket` | Public API | Combinator / iteration | Receives a single datagram from the connected address without removing it from the queue. |
| 1615 | `poll_peek`  | `UdpSocket` | Public API | Poll function | Receives data from the connected address, without removing it from the input queue. |
| 1661 | `try_peek`  | `UdpSocket` | Public API | Non-blocking attempt | Tries to receive data on the connected address without removing it from the input queue. |
| 1711 | `peek_from` 🅰 | `UdpSocket` | Public API | Combinator / iteration | Receives data from the socket, without removing it from the input queue. |
| 1760 | `poll_peek_from`  | `UdpSocket` | Public API | Poll function | Receives data from the socket, without removing it from the input queue. |
| 1811 | `try_peek_from`  | `UdpSocket` | Public API | Non-blocking attempt | Tries to receive data on the socket without removing it from the input queue. |
| 1830 | `peek_sender` 🅰 | `UdpSocket` | Public API | Combinator / iteration | Retrieve the sender of the data at the head of the input queue, waiting if empty. |
| 1859 | `poll_peek_sender`  | `UdpSocket` | Public API | Poll function | Retrieve the sender of the data at the head of the input queue, scheduling a wakeup if empty. |
| 1877 | `try_peek_sender`  | `UdpSocket` | Public API | Non-blocking attempt | Try to retrieve the sender of the data at the head of the input queue. |
| 1884 | `peek_sender_inner`  | `UdpSocket` | Private helper | Combinator / iteration |  |
| 1901 | `broadcast`  | `UdpSocket` | Public API | Data movement | Gets the value of the `SO_BROADCAST` option for this socket. |
| 1909 | `set_broadcast`  | `UdpSocket` | Public API | Configuration / setter | Sets the value of the `SO_BROADCAST` option for this socket. |
| 1918 | `multicast_loop_v4`  | `UdpSocket` | Public API | Networking | Gets the value of the `IP_MULTICAST_LOOP` option for this socket. |
| 1929 | `set_multicast_loop_v4`  | `UdpSocket` | Public API | Configuration / setter | Sets the value of the `IP_MULTICAST_LOOP` option for this socket. |
| 1938 | `multicast_ttl_v4`  | `UdpSocket` | Public API | Networking | Gets the value of the `IP_MULTICAST_TTL` option for this socket. |
| 1951 | `set_multicast_ttl_v4`  | `UdpSocket` | Public API | Configuration / setter | Sets the value of the `IP_MULTICAST_TTL` option for this socket. |
| 1960 | `multicast_loop_v6`  | `UdpSocket` | Public API | Networking | Gets the value of the `IPV6_MULTICAST_LOOP` option for this socket. |
| 1971 | `set_multicast_loop_v6`  | `UdpSocket` | Public API | Configuration / setter | Sets the value of the `IPV6_MULTICAST_LOOP` option for this socket. |
| 2006 | `tclass_v6`  | `UdpSocket` | Public API | Other / internal logic |  |
| 2044 | `set_tclass_v6`  | `UdpSocket` | Public API | Configuration / setter |  |
| 2067 | `ttl`  | `UdpSocket` | Public API | Networking | Gets the value of the `IP_TTL` option for this socket. |
| 2089 | `set_ttl`  | `UdpSocket` | Public API | Configuration / setter | Sets the value for the `IP_TTL` option on this socket. |
| 2118 | `tos_v4`  | `UdpSocket` | Public API | Other / internal logic |  |
| 2148 | `tos`  | `UdpSocket` | Public API | Other / internal logic |  |
| 2182 | `set_tos_v4`  | `UdpSocket` | Public API | Configuration / setter |  |
| 2212 | `set_tos`  | `UdpSocket` | Public API | Configuration / setter |  |
| 2224 | `device`  | `UdpSocket` | Public API | Other / internal logic |  |
| 2240 | `bind_device`  | `UdpSocket` | Public API | Networking |  |
| 2251 | `join_multicast_v4`  | `UdpSocket` | Public API | Networking | Executes an operation of the `IP_ADD_MEMBERSHIP` type. |
| 2260 | `join_multicast_v6`  | `UdpSocket` | Public API | Networking | Executes an operation of the `IPV6_ADD_MEMBERSHIP` type. |
| 2269 | `leave_multicast_v4`  | `UdpSocket` | Public API | Networking | Executes an operation of the `IP_DROP_MEMBERSHIP` type. |
| 2278 | `leave_multicast_v6`  | `UdpSocket` | Public API | Networking | Executes an operation of the `IPV6_DROP_MEMBERSHIP` type. |
| 2302 | `take_error`  | `UdpSocket` | Public API | Data movement | Returns the value of the `SO_ERROR` option. |
| 2314 | `try_from`  | `TryFrom<std::net::UdpSocket> for UdpSocket` | Trait impl | Conversion | Consumes stream, returning the tokio I/O object. |
| 2320 | `fmt`  | `fmt::Debug for UdpSocket` | Trait impl | Formatting |  |
| 2331 | `as_raw_fd`  | `AsRawFd for UdpSocket` | Trait impl | OS handle access |  |
| 2337 | `as_fd`  | `AsFd for UdpSocket` | Trait impl | OS handle access |  |
| 2348 | `as_raw_socket`  | `AsRawSocket for UdpSocket` | Trait impl | OS handle access |  |
| 2354 | `as_socket`  | `AsSocket for UdpSocket` | Trait impl | OS handle access |  |

