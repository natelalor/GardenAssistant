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
    formData.forEach((value, key) => {
      formDataObject[key] = value;
    });

    // now that data is json object, request to backend
    axios.post('http://localhost:5000/process-form', formDataObject)
      .then(response => {
        console.log('Form submitted successfully:', response.data.length, response.data.width, response.data.veggies);
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
          Welcome to the garden assistant tool. Please input below your dream garden's length and width, as well as the specified veggies you'd like to plant from the list. Once you click generate, it will calculate the best optimization for you garden layout based on the guidelines you've provided.
        </p>
      </div>
      <div className="gathering_intel_wrapper">
        <div className="dimensions_wrapper">

          <form id="dimensions-form" action="#" method="post" onSubmit={handleSubmit}>
            <label>Length:</label>
            <input type="text" id="length" placeholder="110"></input>
            <label>Width:</label>
            <input type="text" id="width" placeholder="125"></input>

            <label for="veggies">Veggie Selection List:</label>
            <select name="veggies" id="veggies" multiple>
              <option value="carrots">carrots</option>
              <option value="potatoes">potatoes</option>
              <option value="tomatoes">tomatoes</option>
              <option value="brussel_sprouts">brussel sprouts</option>
              <option value="spinach">spinach</option>
            </select> 
          </form>
        </div>
        <button type="submit" form="dimensions-form">Generate</button>
      </div>
    </>
  )
}

export default App
