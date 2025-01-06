import argparse
import socket
from typing import Optional
import pydantic

class Data(pydantic.BaseModel):
  header: dict[str, str]
  body: str


def get_tcp_data(s: socket.socket) -> Optional[bytes]:
  buffer_size = 1024
  data = b''
  while True:
    buf = s.recv(buffer_size)
    if not buf:
      return None
    data += buf
    if len(buf) < buffer_size:
      break
  return data


def parse_data(data: bytes) -> Data:
  header, body = data.split(b'\r\n\r\n', 1)
  header = dict(
    [k.decode(), v.decode()]
    for line in header.split(b'\n')
    for [k, v] in [line.split(b': ', 1)]
  )
  return Data(header=header, body=body.decode())


def main_tcp_server(port: int) -> None:
  print(f'Listening on localhost:{port}')

  s = socket.create_server(('localhost', port))
  s.listen()
  conn, addr = s.accept()

  with conn:
    print(f'Connected by {addr}')
    while (data := get_tcp_data(conn)) is not None:
      print(f'Received: {data}')
      print(parse_data(data))

  print('Connection closed')


def main_stdio_server() -> None:
  raise NotImplementedError('Not implemented yet')


def parse_args() -> argparse.Namespace:
  parser = argparse.ArgumentParser(description='gofmtls')
  parser.add_argument('-p', '--port', type=int, help='Port to listen on')
  return parser.parse_args()


def main() -> None:
  print('Hello, world!')
  args = parse_args()
  if args.port:
    main_tcp_server(args.port)
  else:
    main_stdio_server()

if __name__ == '__main__':
  main()
