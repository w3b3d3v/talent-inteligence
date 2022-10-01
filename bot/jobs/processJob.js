// get data from db and process it here
module.exports = {
    process: async function(data) {
        console.log(data)
        return;
    },

    storeMessages: async function(data) {
        try {
            const { db  } = require('../../db/db');
            var insertQuery = db.prepare("INSERT or IGNORE INTO messages (text) VALUES (?)");
            for (var i = 0; i < data.length; i++) {
                insertQuery.run(data[i]);
                console.log("Data inserted successfully...");
            }
            insertQuery.finalize();
        }
        
        catch(e) {
            console.log(e);
        }
    }
}
