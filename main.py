from fastapi import FastAPI,Path,HTTPException,Query
import json
app=FastAPI()

def load_data():
    with open('patients.json', 'r') as f:
        data=json.load(f)
        
    return data    
#server par data fetch karne ke liye get
@app.get("/")    
def hello():
    return {'message': 'Patient Management System API'}

@app.get('/about')
def about():
    return {'message': 'This is the about page.Here we can learn about the application and its purpose.'}

@app.get('/view')
def view():
    data=load_data()
    
    return data

@app.get('/view/{patient_id}')
def view_patient(patient_id:str=Path(...,description="The ID of the patient to retrieve",example="1")):
    data=load_data()
    
    #patient=data.get(str(patient_id))
    
    if patient_id in data:
        return data[patient_id]
    # else:
    #     return {'message': 'Patient not found.'}
    raise HTTPException(status_code=404,detail="Patient not found.")

@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description="The field to sort by height,weight or bmi"),order: str = Query('asc', description="The order to sort by asc or desc")):
    # data=load_data()
    # sorted_data=sorted(data.items(), key=lambda x: x[1]['name'])
    # return dict(sorted_data)
    valid_fields = ['height', 'weight', 'bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field. Valid fields are: {', '.join(valid_fields)}")
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid order. Valid orders are: asc, desc")
    data=load_data()
    sort_order=True if order == 'desc' else False
    sorted_data=sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)
    return sorted_data
