import React, { useEffect, useState } from "react";
import API from './api';

function Dashboard() {
    const [metrics, setMetrics] = useState({ total_tasks: 0, pending_tasks: 0, in_progress_tasks: 0, completed_tasks: 0 });
    const [tasks, setTasks] = useState([]);
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [status, setStatus] = useState('Pending');
    const [githubLink, setGithubLink] = useState('');

    const fetchdata = async () => {
        try {
            const metricsRes = await API.get('/dashboard/metrics');
            setMetrics(metricsRes.data);

            const tasksRes = await API.get('/tasks');
            setTasks(tasksRes.data);
        } catch (err) {
            console.error("Error fetching dashboard data");
        }
    };

    useEffect(() => {
        fetchdata();
    }, []);

    const handleCreateTask = async (e) => {
        e.preventDefault();
        try {
            await API.post('/tasks', {
                title,
                description,
                status,
                github_link: githubLink
            });
            setTitle('');
            setDescription('');
            setGithubLink('');
            fetchdata();
        } catch (err) {
            alert('failed to add project task.');
        }
    };

    const handleUpdateStatus = async (taskId, currentStatus) => {
        let nextStatus = "In Progress";
        if (currentStatus === 'In Progress') nextStatus = 'Completed';
        if (currentStatus === 'Completed') nextStatus = 'Pending';

        try {
            await API.put(`/tasks/${taskId}`, { status: nextStatus });
            fetchdata();
        } catch (err) {
            console.error(err);
        }
    };

    const handleDeleteTask = async (taskId) => {
        if (window.confirm("Are you sure you want to delete this task permanently?")) {
            try {
                await API.delete(`/tasks/${taskId}`);
                fetchdata();
            } catch (err) {
                alert("An error occurred while deleting.");
                console.error("Delete call request error", err);
            }
        }
    };

    return (
        <div className="row mt-2">
            <div className="col-md-3 mb-3">
                <div className="card text-white bg-dark shadow p-3 text-center">
                    <h6>Total Projects</h6>
                    <h2>{metrics.total_tasks}</h2>
                </div>
            </div>
            <div className="col-md-3 mb-3">
                <div className="card text-white bg-warning shadow p-3 text-center">
                    <h6>Pending</h6>
                    <h2>{metrics.pending_tasks}</h2>
                </div>
            </div>
            <div className="col-md-3 mb-3">
                <div className="card text-white bg-primary shadow p-3 text-center">
                    <h6>In Progress</h6>
                    <h2>{metrics.in_progress_tasks}</h2>
                </div>
            </div>
            <div className="col-md-3 mb-3">
                <div className="card text-white bg-success shadow p-3 text-center">
                    <h6>Completed</h6>
                    <h2>{metrics.completed_tasks}</h2>
                </div>
            </div>

            <div className="col-md-4 mt-3">
                <div className="card p-3 shadow mb-3">
                    <h5>Log New Build Task</h5>
                    <form onSubmit={handleCreateTask}>
                        <div className="mb-2">
                            <label className="form-label small mb-0">Project/Task Title</label>
                            <input type="text" className="form-control form-control-sm" required value={title} onChange={(e) => setTitle(e.target.value)} />
                        </div>
                        <div className="mb-2">
                            <label className="form-label small mb-0">Description</label>
                            <textarea className="form-control form-control-sm" rows="2" value={description} onChange={(e) => setDescription(e.target.value)}></textarea>
                        </div>
                        <div className="mb-2">
                            <label className="form-label small mb-0">Github Repository Link</label>
                            <input type="url" className="form-control form-control-sm" placeholder="https://github.com..." value={githubLink} onChange={(e) => setGithubLink(e.target.value)} />
                        </div>
                        <div className="mb-3">
                            <label className="form-label small mb-0">Initial Status</label>
                            <select className="form-select form-select-sm" value={status} onChange={(e) => setStatus(e.target.value)}>
                                <option value="Pending">Pending</option>
                                <option value="In Progress">In Progress</option>
                                <option value="Completed">Completed</option>
                            </select>
                        </div>
                        <button type="submit" className="btn btn-dark btn-sm w-100">Add Log</button>
                    </form>
                </div>
            </div>

            <div className="col-md-8 mt-3">
                <div className="card p-3 shadow table-responsive">
                    <h5>Active Iteration Tasks Log</h5>
                    <table className="table table-hover align-middle mt-2 small">
                        <thead className="table-light">
                            <tr>
                                <th>Project Task</th>
                                <th>Description</th>
                                <th>Repository</th>
                                <th>Status</th>
                                <th>Action</th>
                                <th>Delete</th>
                            </tr>
                        </thead>
                        <tbody>
                            {tasks.length === 0 ? (
                                <tr><td colSpan="6" className="text-center text-muted py-3">No tasks tracked yet. Add one to begin!</td></tr>
                            ) : (
                                tasks.map((task) => (
                                    <tr key={task.id}>
                                        <td><strong>{task.title}</strong></td>
                                        <td>{task.description || '-'}</td>
                                        <td>
                                            {task.github_link ? (
                                                <a href={task.github_link} target="_blank" rel="noreferrer" className="text-truncate d-inline-block" style={{maxWidth: '120px'}}>Link</a>
                                            ) : '-'}
                                        </td>
                                        <td>
                                            <span className={`badge ${task.status === 'Completed' ? 'bg-success' : task.status === 'In Progress' ? 'bg-primary' : 'bg-warning text-dark'}`}>
                                                {task.status}
                                            </span>
                                        </td>
                                        <td>
                                            <button className="btn btn-xs p-1 py-0 fs-7" onClick={() => handleUpdateStatus(task.id, task.status)}>🔄</button>
                                        </td>
                                        <td>
                                             <button className="btn btn-outline-danger btn-sm py-0 px-2" title="Delete Task" onClick={() => handleDeleteTask(task.id)}>
                                                Delete
                                            </button>
                                        </td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}

export default Dashboard;
