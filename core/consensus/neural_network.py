import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

class NeuralNetworkConsensus(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(NeuralNetworkConsensus, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

class ConsensusDataset(Dataset):
    def __init__(self, transactions, labels):
        self.transactions = transactions
        self.labels = labels

    def __len__(self):
        return len(self.transactions)

    def __getitem__(self, idx):
        transaction = self.transactions[idx]
        label = self.labels[idx]
        return {
            'transaction': transaction,
            'label': label
        }

def train_neural_network(transactions, labels, epochs=100, batch_size=32):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = NeuralNetworkConsensus(input_dim=256, hidden_dim=128, output_dim=1)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    dataset = ConsensusDataset(transactions, labels)
    data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    for epoch in range(epochs):
        for batch in data_loader:
            transactions_batch = batch['transaction'].to(device)
            labels_batch = batch['label'].to(device)

            optimizer.zero_grad()
            outputs = model(transactions_batch)
            loss = criterion(outputs, labels_batch)
            loss.backward()
            optimizer.step()

            print(f'Epoch {epoch+1}, Loss: {loss.item()}')

    return model

def predict(model, transactions):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    transactions = torch.tensor(transactions).to(device)
    outputs = model(transactions)
    return outputs.detach().cpu().numpy()

# Example usage:
transactions = [...]
labels = [...]
model = train_neural_network(transactions, labels)
predictions = predict(model, transactions)
