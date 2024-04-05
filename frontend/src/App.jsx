import { useState, useEffect } from 'react'
import axios from "axios"
import './App.css'



// TODO LIST:
// - finish setting up form (names, values, submit button(?))
// - mobile view 
// - api
// - fix favicon in index.html not showing up



function App() {
  // const [count, setCount] = useState(0)
  const [data, setData] = useState()
  const [array, setArray] = useState([])

  const fetchAPI = async () => {
    const response = await axios.get("http://127.0.0.1:5000")
    setArray(response.data.users)
  }

  useEffect(() => {
    fetchAPI();
  }, [])


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

          <form id="dimensions-form" action="#" method="post">
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
