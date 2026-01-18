# 🚀 Deployment Guide

This guide covers multiple deployment options for PaperBOT.

---

## 📋 Prerequisites

Before deploying, ensure you have:
- ✅ Pinecone API key (index: `paperbot`, dimensions: `1024`)
- ✅ Google AI API key (Gemini)
- ✅ (Optional) HuggingFace token

---

## 🐳 Option 1: Docker (Recommended)

Docker provides the most consistent deployment across any environment.

### Local Docker Deployment

```bash
# 1. Build the image
docker build -t paperbot .

# 2. Run the container
docker run -d \
  --name paperbot \
  -p 8000:8000 \
  -e PINECONE_API_KEY=your_pinecone_key \
  -e GOOGLE_API_KEY=your_google_key \
  paperbot

# 3. Access at http://localhost:8000
```

### Docker Compose (Easier)

```bash
# 1. Create .env file with your API keys
cp .env.example .env
# Edit .env with your actual keys

# 2. Start the application
docker-compose up -d

# 3. View logs
docker-compose logs -f

# 4. Stop the application
docker-compose down
```

---

## 🚂 Option 2: Railway (Free Tier)

Railway offers easy deployment with a generous free tier.

### Steps

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Deploy from GitHub**
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your `PaperBOT` repository
   - Railway auto-detects Dockerfile

3. **Set Environment Variables**
   - Go to your project → "Variables"
   - Add:
     ```
     PINECONE_API_KEY=your_key
     GOOGLE_API_KEY=your_key
     HF_TOKEN=your_token (optional)
     ```

4. **Generate Domain**
   - Go to "Settings" → "Networking"
   - Click "Generate Domain"
   - Your app is live! 🎉

### Railway Pricing
- **Free Tier**: $5/month credit (enough for light usage)
- **Hobby**: $5/month for 8GB RAM, 8 vCPU

---

## 🎨 Option 3: Render (Free Tier)

Render provides simple deployment with auto-scaling.

### Steps

1. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Deploy Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Select "Docker" as runtime
   - Choose "Free" plan

3. **Configure Environment**
   - Add environment variables:
     ```
     PINECONE_API_KEY=your_key
     GOOGLE_API_KEY=your_key
     ```

4. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes for first build

### Render Pricing
- **Free Tier**: 750 hours/month, sleeps after 15 min inactivity
- **Starter**: $7/month for always-on

---

## ☁️ Option 4: Cloud VPS (Full Control)

For production with full control, use a VPS.

### DigitalOcean / Linode / Vultr

```bash
# 1. Create a VPS (Ubuntu 22.04, 2GB RAM minimum)

# 2. SSH into server
ssh root@your-server-ip

# 3. Install Docker
curl -fsSL https://get.docker.com | sh

# 4. Clone repository
git clone https://github.com/vikash-48413/PaperBOT.git
cd PaperBOT

# 5. Create environment file
cp .env.example .env
nano .env  # Add your API keys

# 6. Start with Docker Compose
docker-compose up -d

# 7. (Optional) Setup Nginx reverse proxy with SSL
apt install nginx certbot python3-certbot-nginx
```

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 300s;
        client_max_body_size 20M;
    }
}
```

---

## 🔧 Configuration for Production

### Modify app.py for Production

The app already binds to `0.0.0.0:8000`, which works for containers.

### Memory Considerations

The embedding model requires ~2GB RAM. Ensure your deployment has:
- **Minimum**: 2GB RAM
- **Recommended**: 4GB RAM

### File Upload Storage

- Uploaded files are stored in `/app/uploads/`
- For persistent storage, mount a volume (see docker-compose.yml)
- Consider using cloud storage (S3, GCS) for production

---

## 🔍 Health Checks

The app exposes `/model_status` for health checks:

```bash
curl http://your-domain.com/model_status
# Returns: {"status": "ready", "model_loaded": true}
```

---

## 🐛 Troubleshooting

### Container won't start
- Check logs: `docker logs paperbot`
- Ensure environment variables are set
- Verify Pinecone index exists

### Out of memory
- The embedding model needs 2GB+ RAM
- Use swap if needed: `fallocate -l 2G /swapfile`
- Consider the "fast" model for less memory usage

### Slow first request
- Normal! The model warms up on first load
- Takes 30-60 seconds initially

---

## 📊 Deployment Comparison

| Platform | Free Tier | Min RAM | Auto Deploy | Custom Domain | SSL |
|----------|-----------|---------|-------------|---------------|-----|
| Railway | $5 credit | 512MB | ✅ | ✅ | ✅ |
| Render | 750 hrs | 512MB | ✅ | ✅ | ✅ |
| Fly.io | 3 VMs | 256MB | ✅ | ✅ | ✅ |
| DigitalOcean | - | 1GB | Manual | ✅ | Manual |
| Docker Local | - | 2GB | - | - | - |

---

## 🎯 Recommendation

For your use case, I recommend:

1. **Just testing?** → Use Docker locally
2. **Free hosting?** → Use Railway (best free tier)
3. **Production?** → Use DigitalOcean + Docker + Nginx
4. **Enterprise?** → Use AWS/GCP with Kubernetes

---

<p align="center">
  <b>Happy Deploying! 🚀</b>
</p>
