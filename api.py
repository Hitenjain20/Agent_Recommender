from fastapi import FastAPI, HTTPException
from inference import Inference


utils = Inference()

app = FastAPI()



@app.post("/query")
async def query(ques):

    try:
        response = utils._query_engine(ques)
        print(response)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", reload=True)