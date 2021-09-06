echo -e "\n███╗   ███╗██╗ ██████╗██████╗  ██████╗ ███████╗ ██████╗  ██████╗██╗ █████╗ ██╗     
████╗ ████║██║██╔════╝██╔══██╗██╔═══██╗██╔════╝██╔═══██╗██╔════╝██║██╔══██╗██║     
██╔████╔██║██║██║     ██████╔╝██║   ██║███████╗██║   ██║██║     ██║███████║██║     
██║╚██╔╝██║██║██║     ██╔══██╗██║   ██║╚════██║██║   ██║██║     ██║██╔══██║██║     
██║ ╚═╝ ██║██║╚██████╗██║  ██║╚██████╔╝███████║╚██████╔╝╚██████╗██║██║  ██║███████╗
╚═╝     ╚═╝╚═╝ ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝╚═╝╚═╝  ╚═╝╚══════╝\n"

echo -e "✨ Starting Microsocial Deployment\n";
cd client

if [ -d "node_modules" ]
then
    echo -e "👍 Dependencies Already Installed - Skipping...\n";
else
    echo -e "🔩 Installing Dependencies\n";
    npm install;
fi

echo -e "🔧 Rebuilding Frontend Client";
npm run build

cd ..

echo -e "\n🔥 Deploying Microsocial\n";
deta deploy

