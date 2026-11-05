import React, {useState} from 'react'
import API from './api'

function Auth({onLoginSuccess}) {
    const [isLogin, setIsLogin] = useState(true);
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        try {
            if (isLogin) {
                const params = new URLSearchParams();
                params.append('username', username);
                params.append('password', password);

                const response = await API.post('/auth/login', params);
                localStorage.setItem('token', response.data.access_token);
                onLoginSuccess();
            } else {
                await API.post('/auth/signup', {username, email,password});
                alert('Registration successful! Please Login.');
                setIsLogin(true);
            }
        } catch (err) {
            setError(err.response?.data?.detail || 'Something went wrong. Try again.');
        }
};

    return (
        <div className="container d-flex justify-content-center align-items-center vh-100">
            <div className="card p-4 shadow" style={{ width: '400px' }}>
                <h3 className="text-center mb-4">{isLogin ? 'Login to DevTracker' : 'Create Account'}</h3>
                
                {error && <div className="alert alert-danger">{error}</div>}

                <form onSubmit={handleSubmit}>
                    <div className="mb-3">
                        <label className="form-label">Username</label>
                        <input type="text" className="form-control" required value={username} onChange={(e) => setUsername(e.target.value)} />
                    </div>

                    {!isLogin && (
                        <div className="mb-3">
                            <label className="form-label">Email</label>
                            <input type="email" className="form-control" required value={email} onChange={(e) => setEmail(e.target.value)} />
                        </div>
                    )}

                    <div className="mb-3">
                        <label className="form-label">Password</label>
                        <input type="password" className="form-control" required value={password} onChange={(e) => setPassword(e.target.value)} />
                    </div>

                    <button type="submit" className="btn btn-primary w-100 mb-3">
                        {isLogin ? 'Login' : 'Sign Up'}
                    </button>
                </form>

                <div className="text-center">
                    <button className="btn btn-link btn-sm text-decoration-none" onClick={() => setIsLogin(!isLogin)}>
                        {isLogin ? "Don't have an account? Sign Up" : 'Already have an account? Login'}
                    </button>
                </div>
            </div>
        </div>
    )
}

export default Auth;
