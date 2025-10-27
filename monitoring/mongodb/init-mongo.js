const dbName = process.env.MONGO_APP_DATABASE || 'myapp';
const username = process.env.MONGO_APP_USERNAME || 'appuser';
const password = process.env.MONGO_APP_PASSWORD || 'apppassword';

db = db.getSiblingDB(dbName);

db.createUser({
  user: username,
  pwd: password,
  roles: [
    {
      role: 'readWrite',
      db: dbName
    }
  ]
});

db.users.insertMany([
  { name: 'John Doe', email: 'john@example.com', created: new Date() },
  { name: 'Jane Smith', email: 'jane@example.com', created: new Date() },
]);

db = db.getSiblingDB('admin');
db.createUser({
  user: 'mongoexporter',
  pwd: 'exporterpassword',
  roles: [
    { role: 'clusterMonitor', db: 'admin' },
    { role: 'read', db: 'local' }
  ]
});

print('Database users created successfully');

print('Database and user created successfully');