import App from './App.svelte';

const app = new App({
    target: document.body,
    props: {
        name: 'Amazing break system',
        backend: '127.0.0.1:5000'
    }
});

export default app;