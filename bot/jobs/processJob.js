// get data from db and process it here
module.exports = {
    process: async function(data) {
        console.log(data)
        return;
    },

    storeMessages: async function(messages, ids) {
        try {
            const { db  } = require('../../db/db');
            var insertQuery = db.prepare("INSERT or IGNORE INTO messages (discordId, text) VALUES (?, ?)");
            for (var i = 0; i < messages.length; i++) {
                insertQuery.run(ids[i], messages[i]);
                console.log("Data inserted successfully...");
            }
            insertQuery.finalize();
        }
        
        catch(e) {
            console.log(e);
        }
    }
}
