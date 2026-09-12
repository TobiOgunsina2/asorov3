import React from 'react'
import Sidebar from "@/components/Sidebar";
import Navbar from '@/components/Navbar';


const Layout = ({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) => {
  return (
    <div className="fixed inset-0 bg-gradient-to-br from-[#f5f0e8] to-[#f0a07a]">
      
      <div className="fixed inset-0 z-0 pointer-events-none">{/* characters, animations live here, can go anywhere */}</div>

      <nav className="fixed top-0 left-0 right-0 z-20 h-20 flex justify-between pt-1 px-8 shadow-sm">
        <Navbar/>
      </nav>

      <aside className="fixed top-36 right-8 bottom-0 w-80 z-10 overflow-y-auto">
        <Sidebar/>
      </aside>

      <div className="absolute top-16 left-0 right-80 bottom-0 overflow-y-auto">
        <main className="">  
          {children}
        </main>
      </div>

    </div>
  )
}

export default Layout