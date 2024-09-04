import { useState } from 'react';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [answer, setAnswer] = useState('');

  const handleQuery = async () => {
    const response = await fetch('/query', {
      method: 'POST',
      headers: {'Content-Type': 'application/json',},
      body: JSON.stringify({query}),
    });
    const data = await response.json();
    setAnswer(data.answer);
  }
  return (
    <div className="App">
      <h1>RAG chatbot</h1>
      <p>ask a question about the ELIT10FinalEssay pdf</p>
      <input type="text" value={query} onChange={(e) => setQuery(e.target.value)} />
      <button onClick={handleQuery}>Submit</button>
      <p>Answer: <br/>{answer}</p>
    </div>
  );
}

export default App;
