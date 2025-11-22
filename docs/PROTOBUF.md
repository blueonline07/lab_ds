# Protocol Buffer Generation

## Regenerating gRPC Code

If you modify `shared/monitoring.proto`, regenerate the Python code with:

```bash
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. shared/monitoring.proto
```

This generates:
- `shared/monitoring_pb2.py` - Message class definitions
- `shared/monitoring_pb2_grpc.py` - Service stubs and client/server code

## Generated Files

Both files are auto-generated and should not be edited manually. The generated code uses relative imports that work with the package structure.

## Files Generated

- `monitoring_pb2.py` - Message class definitions
- `monitoring_pb2_grpc.py` - Service stubs and client/server code

Both files are auto-generated and should not be edited manually (except for the import fix).

