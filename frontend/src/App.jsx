import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'



// TODO LIST:
// - finish setting up form (names, values, submit button(?))
// - mobile view 
// - api
// - fix favicon in index.html not showing up

function App() {
  const [array, setArray] = useState([]);
  const [showResult, setShowResult] = useState(false);
  const [userInput, setUserInput] = useState({
    length: '',
    width: '',
    veggies: []
  });
  const [formData, setFormData] = useState({
    columns: '',
    plants_per_column: '',
    results_list: '',
    veggies: ''
  });

  // tester to verify frontend - backend connection
  useEffect(() => {
    const fetchAPI = async () => {
      try {
        const response = await axios.get('http://localhost:5000/');
        setArray(response.data.users);
      } catch (error) {
        console.error('!! Error fetching data:', error);
      }
      console.log(array)
    };

    fetchAPI();
}, []);

  // function to "override" form submission, using ajax/axios to send
  // form information to backend
  function handleSubmit(event) {
    event.preventDefault(); // this prevents the default form submission
    const formData = new FormData(event.target); // gathern form data
    const formDataObject = {};

    // this is to gather the <select> element options
    formData.forEach((value, key) => {
      if (formDataObject[key]) {
        if (!Array.isArray(formDataObject[key])) {
          formDataObject[key] = [formDataObject[key]];
        }
        formDataObject[key].push(value);
      } else {
        formDataObject[key] = value;
      }
    // console.log("FORM DATA", formData)
    });

    // now that data is json object, request to backend
    axios.post('http://localhost:5000/process-form', formDataObject)
      .then(response => {
        console.log('Form submitted successfully:', response.data.columns, response.data.plants_per_column, response.data.results_list, response.data.veggies);
        // update state with response data to reference later
        setFormData({
          columns: response.data.columns,
          plants_per_column: response.data.plants_per_column,
          results_list: response.data.results_list,
          veggies: response.data.veggies
        });
        setShowResult(true); 
        // this is to change the garden's CSS length & width to be scalable with
        // the user's input for their garden's length & width
        setUserInput({
          length: formDataObject.length,
          width: formDataObject.width,
          veggies: formDataObject.veggies
        });


        // HANDLE RESPONSE HERE! !!!! !!!!


      })
      .catch(error => {
        console.error('ERROR SUBMITTING FORM:', error);
      });
  }

  return (
    <>
      <div className="intro_info_wrapper">
        <h1>Time to Get Planting!</h1>
        <p>
          Please input below your dream garden's length and width, as well as the specified veggies you'd like to plant from the list. Once you click generate, it will calculate the best optimization for you garden layout based on the guidelines you've provided.
        </p>
      </div>
      <div className="gathering_intel_wrapper">
        <div className="dimensions_wrapper">

          <form id="dimensions-form" action="#" method="post" onSubmit={handleSubmit}>
            <label>Length (inches):</label>
            <input type="text" id="length" name="length" placeholder="110" required></input>
            <label>Width (inches):</label>
            <input type="text" id="width" name="width" placeholder="125" required></input>

            <label htmlFor="veggies">Veggie Selection List:</label>
            <select name="veggies" id="veggies" multiple required>
              <option value="Carrot">carrots</option>
              <option value="Potato">potatoes</option>
              <option value="Tomato">tomatoes</option>
              <option value="Brussel Sprout">brussel sprouts</option>
              <option value="Spinach">spinach</option>
            </select> 
            <button type="submit" form="dimensions-form">Generate</button>
          </form>
          <div className="content-container">
          {showResult ? (
            <div className="result-container">
              <div className="result-wrapper" style={{ width: `${userInput.width}px`, height: `${userInput.length}px` }}>
                <p>{formData.columns}</p>
                <p>{formData.plants_per_column}</p>
                <p>{formData.results_list}</p>
                <p>{formData.veggies}</p>
              </div>
            </div>
          ) : (
            <div className="result-container">
              <p>Click generate to get your garden here!</p>
            </div>
          )}
          </div>
        </div>
      </div>
    </>
  )
}

export default App
