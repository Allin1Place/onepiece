const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');

const app = express();
const port = 3000;

// Connect to MongoDB
mongoose.connect('mongodb://localhost:27017/usernames')
  .then(() => console.log('Connected to MongoDB'))
  .catch(err => console.error('Failed to connect to MongoDB', err));

// Define a schema and model for storing usernames
const userSchema = new mongoose.Schema({
  username: String
});

const User = mongoose.model('User', userSchema);

app.use(bodyParser.json());

app.post('/save-username', (req, res) => {
  const username = req.body.username;

  // Save the username to MongoDB
  const user = new User({ username });
  user.save((err) => {
    if (err) {
      res.status(500).send({ message: 'Failed to save username' });
    } else {
      res.status(200).send({ message: 'Username saved successfully' });
    }
  });
});

app.use(express.static('public')); // Serve static files from 'public' directory

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
