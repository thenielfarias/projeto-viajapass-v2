// openModal.test.js
const openModal = require('./openModal'); // Importa a função

// Jest fornece funções de teste
test('abre um modal com sucesso', () => {
  // Configura o ambiente do DOM
  document.body.innerHTML = `
    <div id="modalTeste" style="display: none;"></div>
  `;

  // Chama a função openModal
  openModal('modalTeste');

  // Verifica se a função funcionou corretamente
  const modal = document.getElementById('modalTeste');
  expect(modal.style.display).toBe('block');
});
