import argparse
import json
import socket
import subprocess
from typing import Any, Optional, Self, TypeAlias
import pydantic


class Data(pydantic.BaseModel):
    header: dict[bytes, bytes]
    body: bytes

    @classmethod
    def from_body_bytes_with_parse(cls, body: bytes) -> Self:
        header, body = body.split(b"\r\n\r\n", 1)
        header = dict(line.split(b": ", 1) for line in header.split(b"\n"))
        return cls(header=header, body=body)

    @classmethod
    def from_body_dict(cls, d: dict[str, Any]) -> Self:
        body = json.dumps(d).encode()
        return cls(header={}, body=body)

    def encode(self) -> bytes:
        header = {
            b"Content-Length": str(len(self.body)).encode(),
            **self.header,
        }
        header_bytes = b"\r\n".join(b"%b: %b" % (k, v) for k, v in header.items())
        return header_bytes + b"\r\n\r\n" + self.body


Request: TypeAlias = dict[str, Any]
Response: TypeAlias = Optional[dict[str, Any]]


def get_tcp_data(s: socket.socket) -> Optional[bytes]:
    buffer_size = 1024
    data = b""
    while True:
        buf = s.recv(buffer_size)
        if not buf:
            return None
        data += buf
        if len(buf) < buffer_size:
            break
    return data


def json_rpc_dict(d: dict[str, Any]) -> dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        **d,
    }


def handler_initialize(req: Request) -> Response:
    return {
        "result": {
            "capabilities": {
                "executeCommandProvider": {
                    "commands": ["format"],
                },
            }
        }
    }


def handler_workspace_executeCommand(req: Request) -> Response:
    params = req.get("params", {})
    command = params.get("command")
    arguments = params.get("arguments", [])
    if command == "format":
        filepath = arguments[0]
        print(f"Formatting {filepath}")
        subprocess.run(["go", "fmt", filepath])
        return {
            "result": None,
        }

    print(f"Unknown command: {command}")


handlers = {
    "initialize": handler_initialize,
    "workspace/executeCommand": handler_workspace_executeCommand,
}


def handler(req: Request) -> Response:
    fn = handlers.get(req.get("method"))  # type: ignore
    if fn is None:
        print(f"Unknown method: {req}")
        return None
    return fn(req)


def main_tcp_server(port: int) -> None:
    print(f"Listening on localhost:{port}")

    s = socket.create_server(("localhost", port))
    s.listen()
    conn, addr = s.accept()

    with conn:
        print(f"Connected by {addr}")
        while (raw_data := get_tcp_data(conn)) is not None:
            print(f"Received: {raw_data}")
            data = Data.from_body_bytes_with_parse(raw_data)
            req: dict[str, Any] = json.loads(data.body.decode())
            print(f"Parsed: {req}")
            id_str = req.get("id")
            if id_str is not None:
                res = handler(req)
                print(f"Response: {res}")
                if res:
                    res_data = Data.from_body_dict(json_rpc_dict(dict(res, id=id_str)))
                    conn.sendall(res_data.encode())

    print("Connection closed")


def main_stdio_server() -> None:
    raise NotImplementedError("Not implemented yet")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="gofmtls")
    parser.add_argument("-p", "--port", type=int, help="Port to listen on")
    return parser.parse_args()


def main() -> None:
    print("Hello, world!")
    args = parse_args()
    if args.port:
        main_tcp_server(args.port)
    else:
        main_stdio_server()


if __name__ == "__main__":
    main()
