import argparse

def main_tcp_server(port: int) -> None:
  pass


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
