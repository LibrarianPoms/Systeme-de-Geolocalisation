# Plateforme Web - Environnement de Développement

## 🚀 Démarrage Rapide

### Prérequis
- Node.js 18+ 
- npm ou pnpm
- Navigateur moderne (Chrome, Firefox, Safari, Edge)

### Installation
```bash
# Installation des dépendances
npm install

# Démarrage du serveur de développement
npm start

# Build pour production
npm run build
```

## 📁 Structure du Projet

```
dev/
├── 📁 src/                      # Code source
│   ├── 📁 components/           # Composants React
│   │   ├── 📁 common/          # Composants réutilisables
│   │   ├── 📁 dashboard/       # Composants dashboard
│   │   ├── 📁 map/            # Composants cartographie
│   │   ├── 📁 charts/         # Composants graphiques
│   │   ├── 📁 alerts/         # Composants alertes
│   │   ├── 📁 reports/        # Composants rapports
│   │   ├── 📁 navigation/     # Composants navigation
│   │   └── 📁 admin/          # Composants admin
│   ├── 📁 pages/              # Pages principales
│   ├── 📁 store/              # Redux Toolkit store
│   │   └── 📁 slices/         # Redux slices
│   ├── 📁 services/           # Services API
│   ├── 📁 utils/              # Utilitaires
│   ├── 📁 hooks/              # Hooks personnalisés
│   ├── 📁 types/              # Types TypeScript
│   ├── 📄 App.tsx             # Composant principal
│   ├── 📄 main.tsx            # Point d'entrée
│   └── 📄 index.css           # Styles globaux
├── 📁 public/                 # Fichiers statiques
│   └── 📄 index.html          # Template HTML
├── 📁 docs/                   # Documentation technique
├── 📁 tests/                  # Tests
├── 📁 scripts/                # Scripts de build
├── 📄 package.json            # Dépendances et scripts
├── 📄 vite.config.ts          # Configuration Vite
├── 📄 tsconfig.json           # Configuration TypeScript
└── 📄 README.md               # Ce fichier
```

## 🛠️ Technologies Utilisées

### Frontend
- **React 18** avec TypeScript
- **Vite** pour le build et développement
- **Redux Toolkit** pour la gestion d'état
- **React Router** pour la navigation
- **CSS3** avec variables CSS

### Outils de Développement
- **ESLint** pour la qualité du code
- **Prettier** pour le formatage
- **Jest** pour les tests unitaires
- **React Testing Library** pour les tests composants

## 📋 Scripts Disponibles

```bash
# Développement
npm start              # Démarrer serveur de développement
npm run dev            # Alias pour npm start

# Build
npm run build          # Build pour production
npm run preview        # Prévisualiser build production

# Tests
npm test               # Lancer les tests
npm run test:watch     # Tests en mode watch
npm run test:coverage  # Tests avec couverture

# Qualité
npm run lint           # Vérifier le code
npm run lint:fix       # Corriger automatiquement
npm run format         # Formater le code
npm run type-check     # Vérifier les types TypeScript
```

## 🎨 Architecture des Composants

### Structure des Composants
```typescript
// Exemple de structure composant
interface ComponentProps {
  // Propriétés du composant
}

export const Component: React.FC<ComponentProps> = ({ ...props }) => {
  // Logique du composant
  return (
    <div className="component">
      {/* JSX du composant */}
    </div>
  )
}
```

### Convention de Nommage
- **Composants**: PascalCase (ex: `VehicleList`)
- **Fichiers**: PascalCase.tsx (ex: `VehicleList.tsx`)
- **CSS**: PascalCase.css (ex: `VehicleList.css`)
- **Hooks**: camelCase avec préfixe `use` (ex: `useVehicles`)

## 🔄 Gestion d'État (Redux Toolkit)

### Structure du Store
```typescript
// Slice example
const slice = createSlice({
  name: 'feature',
  initialState,
  reducers: {
    // Actions synchrones
  },
  extraReducers: (builder) => {
    // Actions async
  }
})
```

### Hooks personnalisés
```typescript
// Hook pour utiliser le store
export const useAppDispatch = () => useDispatch<AppDispatch>()
export const useAppSelector = <T>(selector: (state: RootState) => T) => 
  useSelector(selector)
```

## 🎯 Fonctionnalités Implémentées

### ✅ Complètes
- Architecture React + TypeScript
- Configuration Redux Toolkit
- Routage avec React Router
- Layout principal avec Header/Sidebar/Footer
- Pages de base (Dashboard, Flotte, Navigation, etc.)
- Système de thèmes (light/dark/high-contrast)

### 🚧 En Développement
- Composants spécialisés (cartes, graphiques, etc.)
- Services API
- Tests unitaires
- Documentation complète

## 🔧 Configuration

### Variables d'Environnement
```bash
# .env.development
VITE_API_URL=http://localhost:3001
VITE_MAP_API_KEY=your_map_api_key

# .env.production
VITE_API_URL=https://api.geoloc-pl.com
VITE_MAP_API_KEY=production_map_api_key
```

### Personnalisation
- **Thèmes**: Modifier `src/index.css` variables CSS
- **Routes**: Ajouter dans `src/App.tsx`
- **Store**: Ajouter slices dans `src/store/`
- **Composants**: Créer dans dossiers thématiques

## 📱 Développement

### Bonnes Pratiques
1. **TypeScript**: Utiliser des types stricts
2. **Components**: Petits et réutilisables
3. **State**: Gestion centralisée avec Redux
4. **CSS**: Variables CSS pour la cohérence
5. **Tests**: Couverture minimale 80%

### Git Hooks (recommandé)
```bash
# Pre-commit
npm run lint
npm run type-check

# Pre-push
npm test
```

## 🚨 Dépannage

### Problèmes Communs
- **Port 3000 occupé**: Modifier `vite.config.ts`
- **Types manquants**: `npm install @types/...`
- **Build lent**: Vérifier les imports inutiles

### Performance
- **Lazy loading**: `React.lazy()` pour les pages
- **Code splitting**: Configuration Vite
- **Optimization**: `npm run build --analyze`

## 📚 Documentation Complète

- [Documentation technique](../PLATEFORME_WEB_COMPLETE.md)
- [Guide de développement](./docs/development-guide.md)
- [API Reference](./docs/api-reference.md)
- [Composants](./docs/components.md)

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature
3. Faire les changements
4. Ajouter des tests
5. Soumettre une Pull Request

---

*Développé avec ❤️ pour la gestion de flottes de poids lourds*
