const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const port = 3000; // Escolha a porta desejada

// Use o body-parser para processar o corpo das solicitações como JSON
app.use(bodyParser.json());

// Lista fixa de interesses com título e descrição
const availableInterests = [
  { title: 'Interesse 1', description: 'Descrição do Interesse 1' },
  { title: 'Interesse 2', description: 'Descrição do Interesse 2' },
  // Adicione mais interesses conforme necessário
];

// Estrutura para armazenar os registros de clientes
const clientRegistrations = [];

// Rota para consultar a lista de interesses disponíveis
app.get('/available-interests', (req, res) => {
  res.status(200).json(availableInterests);
});

// Rota para gerenciar a lista de interesses
app.post('/manage-interests', (req, res) => {
  // Implemente a lógica para manipular a lista de interesses (adicionar/remover)

  // Exemplo: Adicionar um novo interesse à lista
  const newInterest = req.body;
  availableInterests.push(newInterest);

  res.status(200).json({ message: 'Interesse adicionado com sucesso', interest: newInterest });
});

// Rota para registrar um novo cliente e seus interesses
app.post('/register', (req, res) => {
  const { endpoint, interests } = req.body;

  // Verifique se os interesses fornecidos pelo cliente estão na lista de interesses disponíveis
  const validInterests = interests.filter((interest) =>
    availableInterests.some((availableInterest) => availableInterest.title === interest)
  );

  // Registre o cliente apenas com interesses válidos
  clientRegistrations.push({ endpoint, interests: validInterests });
  console.log(`Cliente registrado: ${endpoint} - Interesses: ${validInterests}`);
  res.status(200).send('Registro bem-sucedido!');
});

// Rota para o evento a ser acionado
app.post('/trigger-event', (req, res) => {
  const eventData = req.body;

  // Itera sobre os registros de clientes e envia dados para os interesses correspondentes
  clientRegistrations.forEach((registration) => {
    const { endpoint, interests } = registration;

    // Verifique se há algum interesse correspondente ao evento
    if (interests.includes(eventData.interest)) {
      // Implemente aqui a lógica para enviar os dados para os endpoints registrados
      console.log(`Enviando dados para ${endpoint} com interesse ${eventData.interest}:`, eventData);
      // Você pode usar bibliotecas como axios para enviar requisições HTTP aos endpoints registrados
    }
  });

  res.status(200).send('Evento processado e enviado para endpoints registrados.');
});

// Inicie o servidor
app.listen(port, () => {
  console.log(`Servidor do Webhook está rodando em http://localhost:${port}`);
});
