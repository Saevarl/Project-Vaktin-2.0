import { BrowserRouter as Router, Route, Link, Routes } from 'react-router-dom';
import GPUs from './gpus/pages/gpus';

function App() {
  return (
    <Router>
      <div className="min-h-screen flex flex-col bg-gray-900 text-gray-200">
        <nav className="bg-gray-800 p-4">
          <ul className="flex space-x-4">
            <li>
              <Link to="/" className="text-blue-400 hover:text-blue-300">Home</Link>
            </li>
            <li>
              <Link to="/gpus" className="text-blue-400 hover:text-blue-300">GPUs</Link>
            </li>
          </ul>
        </nav>

        <main className="flex-grow p-6">
          <Routes>
            <Route path="/" element={
              <div className="container mx-auto">
                <h1 className="text-3xl font-bold mb-4 text-white">Home Page</h1>
                <p>Welcome to the home page!</p>
              </div>
            } />
            <Route path="/gpus" element={<GPUs />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;