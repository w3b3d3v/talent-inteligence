const sqlite3 = require('sqlite3').verbose();

const db =  new sqlite3.Database('./db/messages.db', (err) => {
  if (err) {
    return console.error(err.message);
  }
  console.log('Connected to the in-memory SQlite database.');
});

function createTables(db) {
  db.serialize(function() {
    db.run('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT, unique (text))');
  });
}

function deleteTable(db) {
  db.serialize(function() {
    db.run('DROP TABLE messages');
  });
}

function closeDb(db) {
  db.close((err) => {
    if (err) {
      console.error(err.message);
    }
    console.log('Close the database connection.');
  });
}


module.exports = { db, createTables, closeDb, deleteTable }


