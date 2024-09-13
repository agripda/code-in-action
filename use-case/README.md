## NextGenAI Use-Case: Code-In-Action
This is a PoC of Code in Action with NextGenAI Workflows.

### File Structure
search_app/
|-- app.py
|-- models.py
|-- database_setup.py
|-- templates/
    |-- index.html
|-- static/
    |-- style.css
|-- requirements.txt


### Running the Application
Set up a virtual environment and install the required packages:

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Initialize the database and populate it with sample data:

python database_setup.py
Run the Flask application:

python app.py

Open your browser and go to http://127.0.0.1:5000 to see the search functionality in action.

### References
- Workflow: From-User-Story-to-Code-in-Action
- Artifact: http://www.bdax.com.au/toto/use-case/ba-to-script/artifact-solution-design-to-script.html
