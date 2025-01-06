import argparse
import socket

def main_tcp_server(port: int) -> None:
  print(f'Listening on localhost:{port}')

  s = socket.create_server(('localhost', port))
  s.listen()
  conn, addr = s.accept()

  with conn:
    print(f'Connected by {addr}')
    while True:
      data = conn.recv(1024)
      if not data:
        break
      conn.sendall(data)
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
