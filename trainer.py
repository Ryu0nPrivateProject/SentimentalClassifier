import torch
from tqdm import tqdm
from dataloader import dataloader
from torch.cuda import is_available
from transformers import BertForSequenceClassification, BertTokenizer, AdamW

# model_checkpoint = 'monologg/kobert'
model_checkpoint = 'klue/bert-base'


def train_sentimental_classifier(num_epochs=5, batch_size=16):
    device = 'cuda' if is_available() else 'cpu'
    model = BertForSequenceClassification.from_pretrained(model_checkpoint)
    optim = AdamW(model.parameters(), lr=2e-5)
    train_dataloader = dataloader(is_train=True, batch_size=batch_size)

    for epoch in range(num_epochs):
        total_loss = 0
        train_dataloader = tqdm(train_dataloader, leave=True)

        for batch in train_dataloader:
            optim.zero_grad()
            outputs = model(**batch)
            loss = outputs.loss
            loss.backward()
            optim.step()
            loss_val = loss.item()
            total_loss += loss_val
            train_dataloader.set_postfix(loss=loss_val)

        avg_loss = round(total_loss / len(train_dataloader), 3)
        save_model_checkpoint = f'{model.__class__.__name__}_epoch_{epoch}_loss_{avg_loss}.pt'
        model.save_pretrained(save_model_checkpoint)

    return save_model_checkpoint


def evaluate_sentimental_classifier(save_model_checkpoint):
    pass


if __name__ == "__main__":
    save_model_checkpoint = train_sentimental_classifier(1, 4)
    evaluate_sentimental_classifier(save_model_checkpoint)