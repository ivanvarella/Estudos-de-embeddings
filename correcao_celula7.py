# Célula 7 corrigida
def load_20newsgroups_subset():
    """
    Carrega um subconjunto balanceado do 20 Newsgroups com 10 classes selecionadas.
    Retorna textos, labels e metadados.
    """
    # Classes selecionadas para o estudo (diversas e interessantes)
    selected_categories = [
        'alt.atheism',
        'comp.graphics', 
        'comp.sys.mac.hardware',
        'misc.forsale',
        'rec.autos',
        'rec.sport.baseball',
        'sci.crypt',
        'sci.med',
        'soc.religion.christian',
        'talk.politics.guns'
    ]
    
    print("🔄 Carregando 20 Newsgroups...")
    
    # Carregar dados
    newsgroups = fetch_20newsgroups(
        subset='all',
        categories=selected_categories,
        remove=('headers', 'footers', 'quotes'),
        shuffle=True,
        random_state=42
    )
    
    # Criar DataFrame - CORREÇÃO AQUI
    df = pd.DataFrame({
        'text': newsgroups.data,
        'category': [newsgroups.target_names[i] for i in newsgroups.target],  # CORRIGIDO
        'target': newsgroups.target
    })
    
    # Limpeza básica
    df['text'] = df['text'].str.strip()
    df = df[df['text'].str.len() > 50]  # Remover textos muito curtos
    
    print(f"✅ Dataset carregado: {len(df)} documentos")
    print(f"📊 Classes: {df['category'].nunique()}")
    print(f"📈 Distribuição por classe:")
    
    # Mostrar distribuição
    class_counts = df['category'].value_counts()
    for category, count in class_counts.items():
        print(f"   {category}: {count} documentos")
    
    return df

# Carregar dados
df = load_20newsgroups_subset()

# Mostrar exemplos
print(f"\n📝 Exemplos de textos por classe:")
print("=" * 80)
for category in df['category'].unique()[:3]:  # Mostrar apenas 3 classes
    sample_text = df[df['category'] == category]['text'].iloc[0]
    print(f"\n🔹 {category}:")
    print(f"   {sample_text[:200]}...")
    print("-" * 80)
