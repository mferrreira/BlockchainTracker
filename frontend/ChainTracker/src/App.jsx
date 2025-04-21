import { useState, useEffect } from 'react'
import Header from './components/Header'
import Footer from './components/Footer'
import './App.css'

function App() {
  const [solanaTransactions, setSolanaTransactions] = useState([])
  const [ethereumTransactions, setEthereumTransactions] = useState([])
  const [baseTransactions, setBaseTransactions] = useState([])
  
  useEffect(() => { 

    const fetchData = async () => {
      try {
        const solanaResponse = await fetch('http://localhost:5000/transactions?network=solana')
        const parsedResponse = await solanaResponse.json()
        setSolanaTransactions(parsedResponse)

        const ethereumResponse = await fetch('http://localhost:5000/transactions?network=ethereum')
        const parsedEthereumResponse = await ethereumResponse.json()  
        
        setEthereumTransactions(parsedEthereumResponse)
        const baseResponse = await fetch('http://localhost:5000/transactions?network=base')
        const parsedBaseResponse = await baseResponse.json()
        
        setBaseTransactions(parsedBaseResponse)
      } catch (error) {
        console.error('Error fetching data:', error)
      }
    }
    fetchData()
  }, [])

  return (
    <>
      <Header/>
      <main className="container mx-auto p-4 min-h-screen">
        <div className="flex flex-col items-center">
      <h1 className="text-3xl font-bold mb-4">ChainTracker</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 w-full">

      {[
        { title: "Solana", data: solanaTransactions }, 
        { title: "Ethereum", data: ethereumTransactions }, 
        { title: "Base", data: baseTransactions }
      ].map(({ title, data }) => (
        <div key={title} className="bg-white shadow-md rounded-lg p-4 max-w-sm break-words overflow-x-auto w-full">
          <div className='bg-gray-100 p-4 rounded-lg'>
            <h2 className="text-xl font-semibold mb-2">{title} Transactions</h2>
            <ul>
              {data.map((transaction) => (
                <li key={transaction.transaction_id} className="border-b py-2">
                  <p className="text-sm font-mono font-bold">Transaction ID: {transaction.transaction_id}</p>
                  <p>From: {transaction.from_address}</p>
                  <p>To: {transaction.to_address}</p>
                  <p>Amount: {transaction.amount}</p>
                </li>
              ))}
            </ul>
          </div>

          </div>
      ))}
    </div>
  </div>
</main>
      <Footer/>
    </>
  )
}

export default App
