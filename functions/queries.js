require('dotenv').config({ path: 'C:/Users/dantf/Documents/projeto-viajapass/config.env' });

const { Client } = require('pg');
const connectionString = `postgresql://postgres:${process.env.DB_PASSWORD}@localhost:5432/vjps`;

const client = new Client({
	connectionString: connectionString
});
client.connect();

module.exports.insert = function (nome, email, telefone, checkin, pax, gb, destino, res, req) {
	const query = {
		text: 'INSERT INTO vendas(nome, email, telefone, checkin, pax, gb, destino) VALUES($1, $2, $3, $4, $5, $6, $7) RETURNING *;',
		values: [nome, email, telefone, checkin, pax, gb, destino]
	}
	
	if(!req.session.nome){
		client.query(query, (err, res2) => {
		  if (err) {
			console.log(err.stack);
		  } else {
				res.redirect('gateway-payment.html');
		  }
		});
	}
}
