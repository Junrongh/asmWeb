
plt.figure(figsize=(24,24))
cm = plt.cm.get_cmap('RdYlBu') 
plt.scatter(x_tsne[0:418,0], x_tsne[0:418,1], s=100, label='Al', cmap=cm)
plt.scatter(x_tsne[419:718,0], x_tsne[419:718,1], s=100, label='Ci', cmap=cm)
plt.scatter(x_tsne[2190:2636,0], x_tsne[2190:2636,1], s=100, label='Cu', cmap=cm)
plt.scatter(x_tsne[2637:2898,0], x_tsne[2637:2898,1], s=100, label='Ti', cmap=cm)
plt.scatter(x_tsne[719:2189,0], x_tsne[719:2189,1], s=100, label='Cs', cmap=cm)

legend = plt.legend(loc='upper left', shadow=True, fontsize='xx-large')
plt.axis('off')

plt.savefig('../map/ntsne.png')