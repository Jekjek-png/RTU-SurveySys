# RTU_SSA - API CONTRACTS

**BASE URL:** [http://localhost:8000](http://localhost:8000)  
pwede kayo mag base sa lesson na ginawa ni sir

## ENDPOINTS

### 1. SCHOOL SERVICES
- **Method:** GET
- **URL endpoint:** /services
- **NOTE:** ito yung tatlong gagawan na services
- **Request body:** wala
- **Response body:** 200 OK
```json
{
  "services": [
    {
      "service_id": "SVC001",
      "service_name": "Accounting"
    },
    {
      "service_id": "SVC002",
      "service_name": "Registrar"

    },
    {
      "service_id": "SVC003",
      "service_name": "Clinic"
    }
  ]
}
```

### 2. Submit Survey Response
- **Method:** POST
- **URL endpoint:** /response
- **NOTE:** hindi pa final need natin yung mismong survey form na paper

- **Request body:**
```json
{
  "service_id":        "SVC001",
  "Service_Availed":      "Regi form",
  "Respondent_Name":      "Jake Icasiano",
  "Date_of_Visit":        "15/01/2026",
  "Age_Bracket":          "18-20",
  "Gender":               "Male",
  "Category_of_Respondent":"Student",
  "CC1":                  "Box1",
  "CC2":                  "Box1",
  "CC3":                  "Box1",
  "Service_satisfaction(1-5)":"4",
  "Service_Time(1-5)":     "4" ,
  "Service_Requirements(1-5)":"4",
  "Service_Steps(1-5)":    "4",
  "Service_Transaction(1-5)":"4", 
  "Service_Fee(1-5 or N/A)":"4",
  "Service_fair(1-5)":     "4",
  "Service_Courtesy(1-5)": "4",
  "Service_Request(1-5)":  "4",
  "comments/suggestions": "Mainit sa office",
  "Attending_Employee":   "Elijah",
  "comments/suggestions_for_employee":"Masungit"
}
```
- **fields:** lahat ng fields required ng input

- **Response body:** (200 OK)
```json
{
  "message": "Survey submitted successfully.",
  "submitted_at": "2025-05-11T14:32:00"
}
```

- **Error response:**
  - 404 - service id not found
  - 422 - missing required field/s

### 3. Get Responses by Service
- **Method:** GET
- **URL:** /responses?service=Accounting
- **Description:** Returns all survey responses for a specific service. Used by the admin dashboard to display the comments tab.
- **NOTE:** IBA IBA ITO PER SERVICE. Kung 
 - /responses?service=Accounting is for accounting
 - /responses?service=Clinic is for clinic
 - /responses?service=Registrar is for registrar. but pareho lang sila ng response body magkakaiba lang name ng dept

- **Request body:** wala
- **Response body:** (200 OK)
```json
{
  "service": "Accounting",
  "total_responses": 24,
  "responses": [
    {
    "service_id": "SV003",
    "service_availed": "Enrollment form",
    "respondent_name": "Elijahh",
    "date_of_visit": "15/05/2026",
    "age_bracket": "18-20",
    "gender": "Male",
    "category_of_respondent": "Student",
    "cc1": "yes",
    "cc2": "yes",
    "cc3": "yes",
    "service_satisfaction": 5,
    "service_time": 5,
    "service_requirements": 5,
    "service_steps": 5,
    "service_transaction": 5,
    "service_fee": "5",
    "service_fair": 5,
    "service_courtesy": 5,
    "service_request": 4,
    "comments_suggestions": "N/A",
    "attending_employee": "Fey mam",
    "comments_suggestions_for_employee": "mabait"
    }
  ]
}
```


- **Error response:**
  - 404 - Service name not found
  - 422 - service parameter missing from URL

### 4. Admin Login
- **Method:** POST
- **URL:** /admin/login
- **Description:** Validates admin credentials against admins.csv. On success, returns the service the admin is assigned to. Streamlit must save assigned_service in st.session_state after a successful login.

- **Request body:**

```json
{
  "username": "admin_accounting",
  "password": "password123"
}
```
- **fields:** username and password yung required fields for admin login

- **Response body:** (200 OK)
```json
{
  "message": "Login successful.",
  "admin_id": "ADM001",
  "username": "admin_accounting",
  "assigned_service": "Accounting"
}
```

- **Error Responses:**
  - 401 - Wrong username or password — {"detail": "Invalid username or password."}

### 5. Get Admin Summary
- **Method:** GET
- **URL:** /admin/summary?service=Accounting
- **Description:** Returns computed analytics for a service — average ratings, response count, and recent comments and suggestions. Used to populate the admin dashboard charts and metrics.

- **NOTE:** IBA IBA ITO PER SERVICE. Kung 
 - /admin/summary?service=Accounting is for accounting
 - /admin/summary?service=Clinic is for clinic
 - /admin/summary?service=Registrar is for registrar. but pareho lang sila ng response body magkakaiba lang name ng dept

- **Query Parameter:**
  - **Parameter:** service
  - **Required:** Yes
  - **Description:** Must match the logged-in admin's assigned_service
- **Request Body:** None

- **Response body:** (200 OK)

```json
{
  "service": "Accounting",
  "total_responses": 24,
  "average_ratings": {
    "staff":      3.8,
    "speed":      2.9,
    "accuracy":   4.1,
    "facilities": 3.5,
    "overall":    3.7
  },
  "recent_comments": [
    "Staff are polite but queues are long.",
    "Please add more payment terminals."
  ],
  "recent_suggestions": [
    "Longer office hours would help.",
    "Online payment option please."
  ]
}
```

- **Error Responses:**
  - 404 - Service name not found
  - 422 - service parameter missing from URL




### 6. Get export as pdf
- **Method:** GET
- **URL:** 
    /admin/export/pdf?service=Accounting → PDF of Accounting responses
    /admin/export/pdf?service=Registrar → PDF of Registrar responses
    /admin/export/pdf?service=Clinic → PDF of Clinic responses
- **NOTE:** calls this when an admin clicks the Download PDF button. This endpoint does NOT return JSON. It returns a raw PDF file.
- **RESPONSE:**Response (200 OK):
    Content-Type: application/pdf
    Content-Disposition: attachment; filename="Accounting_responses.pdf"
- **ADDITIONAL NOTE:** Ganto daw mukha pag sa streamlit 
 
 ```python 
# example usage in 05_dashboard.py
service = st.session_state["service"]
response = httpx.get(f"http://localhost:8000/admin/export/pdf?service={service}")

st.download_button(
    label="Download PDF Report",
    data=response.content,       # raw PDF bytes, not JSON
    file_name=f"{service}_responses.pdf",
    mime="application/pdf"
)
``` 

- **ERROR RESPONSE** 
 - 404 Not FoundThe service name in the URL does not exist
 - 422 UnprocessableThe ?service= parameter was not included in the URL
 - 500 Server ErrorSomething went wrong while generating the PDF

## Additional Notes
- Ratings must always be integers between 1 and 5. FastAPI will reject anything outside this range with a 422 error.
- Streamlit must never read or write CSV files directly. All data goes through the API.
- After a successful /admin/login, save assigned_service using st.session_state["service"] = response["assigned_service"] and use it for all subsequent admin API calls.
- Both servers must be running at the same time. Open two terminals:

  Terminal 1: uvicorn main:app --reload (inside /backend)  
  Terminal 2: streamlit run app.py (inside /frontend)

