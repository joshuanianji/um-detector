const functions = require("firebase-functions");

const express = require('express');
const app = express();
// // Create and Deploy Your First Cloud Functions
// // https://firebase.google.com/docs/functions/write-firebase-functions

//

app.post('/audio', () => {
    return;
});

exports.helloWorld = functions.https.onRequest((request, response) => {
   functions.logger.info("Hello logs!", {structuredData: true});
   response.send("Hello from Firebase!");
 });


 exports.onStorageUpdate = functions.storage.object().onFinalize( async (object) => {
    functions.logger.info("Hi trigger logs!", {structuredData: true});
    console.log("wow the trigger actually fired");

    const fileBucket = object.bucket; // The Storage bucket that contains the file.
    const filePath = object.name; // File path in the bucket.
    const contentType = object.contentType; // File content type.
    const metageneration = object.metageneration; // Number of times metadata has been generated. New objects have a value of 1.

    console.table({fileBucket, filePath, contentType, metageneration, object});
 });