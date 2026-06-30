require('dotenv').config();
const { MongoClient } = require('mongodb');

const uri = process.env.MONGODB_URI;
const client = new MongoClient(uri);

async function run() {
  try {
    const database = client.db('lumis');
    const collection = database.collection('products');

    const index = {
      name: 'lumis_vector_index',
      type: 'vectorSearch',
      definition: {
        fields: [
          {
            type: 'vector',
            path: 'embedding',
            numDimensions: 384,
            similarity: 'cosine'
          },
          {
            type: 'filter',
            path: 'category'
          },
          {
            type: 'filter',
            path: 'brand'
          },
          {
            type: 'filter',
            path: 'price'
          }
        ]
      }
    };

    const result = await collection.createSearchIndex(index);
    console.log('Index created:', result);
  } finally {
    await client.close();
  }
}

run().catch(console.dir);