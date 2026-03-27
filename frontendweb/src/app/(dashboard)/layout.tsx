import React from 'react'
import "./globals.css";
import Sidebar from "@/components/Sidebar";
import Header from '@/components/Header';


const Layout = ({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) => {
  return (
    <>
      <Header/>
      <div className='content'>
        <main>
          {children}
        </main>
        <Sidebar/>
      </div>
    </>
  )
}

export default Layout