import { BrowserRouter as Router, Route, Link, Routes } from 'react-router-dom';
import GPUs from './gpus/pages/gpus';

function App() {
  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
            <li>
              <Link to="/gpus">GPUs</Link>
            </li>
          </ul>
        </nav>

        <Routes>
          <Route path="/" element={
            <div>
              <h1>Home Page</h1>
              <p>Welcome to the home page!</p>
            </div>
          } />
          <Route path="/gpus" element={<GPUs />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
