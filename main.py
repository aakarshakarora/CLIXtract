import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from common.utils import parse_cli_output
from schema.request import ParseRequest
from schema.response import ParseResponse

app = FastAPI(title="CLIXtract")


@app.get("/version")
def get_version():
    version_data = json.loads((Path(__file__).parent / "version.json").read_text())
    return version_data


@app.post("/parse-cli", response_model=ParseResponse)
async def parse(request: ParseRequest):
    result = await parse_cli_output(
        command_output=request.command_output,
        command_name=request.command_name,
        user_instruction=request.user_instruction,
    )
    return JSONResponse(content={"parsed_output": result})
