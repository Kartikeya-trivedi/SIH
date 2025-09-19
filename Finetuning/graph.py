import matplotlib.pyplot as plt

# Example data: replace these lists with your actual epoch results
epochs = list(range(1, 26))[:25]  # Epochs from 1 to 25

# Replace these values with your actual training loss and validation accuracy from each epoch
training_loss = [2.0641, 1.7354, 1.4761, 1.2632, 1.0983, 1.0174, 0.9001, 0.7730, 0.6849, 0.6161,
                 0.5814, 0.5198, 0.5014, 0.4664, 0.4500, 0.4268, 0.3882, 0.3853, 0.3530, 0.3530,
                 0.3548, 0.3529, 0.2979, 0.2892, 0.2804]

validation_accuracy = [73.33, 77.78, 80, 80, 81.11, 94.44, 96.67, 95.56, 95.56, 96.67,
                       96.67, 96.67, 94.44, 95.56, 95.56, 96.67, 97.78, 97.78, 95.56, 96.67,
                       96.67, 96.67, 96.67, 96.67, 95.56]  

# Plotting Training Loss
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(epochs, training_loss, marker='o', color='red')
plt.title('Training Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.grid(True)

# Plotting Validation Accuracy
plt.subplot(1, 2, 2)
plt.plot(epochs, validation_accuracy, marker='o', color='green')
plt.title('Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy (%)')
plt.grid(True)

plt.tight_layout()
plt.show()
