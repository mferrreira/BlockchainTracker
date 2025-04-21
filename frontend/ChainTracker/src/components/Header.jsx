import React, { useState } from 'react'
import axios from 'axios'

export default function Header() { 
    const [showForm, setShowForm] = useState(false)

    const toggleForm = () => {
      setShowForm((prev) => !prev)
    }

    const handleSubmit = (e) => {
      e.preventDefault()
      const formData = new FormData(e.target)
      const walletAddress = formData.get('walletAddress')
      const blockchain = formData.get('blockchain')

      // Aqui você pode fazer a chamada para a API para adicionar a carteira
      axios.post('http://localhost:5000/wallets', {
        walletAddress,
        blockchain
      })

      // Limpar o formulário após o envio
      e.target.reset()
      setShowForm(false)
    }


    return (
        <header className="bg-gray-800 text-white p-4 flex justify-between items-center">
      <div className="flex items-center gap-4">
        <h1 className="text-xl font-bold">ChainTracker</h1>
        <button 
          onClick={toggleForm}
          className="bg-blue-500 hover:bg-blue-600 px-3 py-1 rounded">
          + Adicionar Carteira
        </button>
      </div>

      {showForm && (
        <div className="bg-white text-black mt-4 p-4 rounded shadow w-full max-w-md">
          <form onSubmit={handleSubmit}>
            <label className="block mb-2">
              Endereço da carteira:
              <input 
                type="text" 
                className="mt-1 p-2 w-full border rounded"
                placeholder="0x..." />
            </label>
            <label className="block mb-2">
              Blockchain:
              <select className="mt-1 p-2 w-full border rounded">
                <option value="solana">Solana</option>
                <option value="ethereum">Ethereum</option>
                <option value="base">Base</option>
              </select>
            </label>
            <button 
              type="submit" 
              className="mt-2 bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded">
              Adicionar
            </button>
          </form>
        </div>
      )}
        </header>
    )
}